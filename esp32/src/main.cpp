#include <Arduino.h>
#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>

//=====================================
// Environment Configuration
//=====================================
#define DEV_MODE true  // true = Wokwi/Simulação, false = Arduino Real

#if !DEV_MODE
    #include <SPIFFS.h>
#endif

//=====================================
// Pin Definitions
//=====================================
#define DHT_PIN 22     // DHT22: Sensor de temperatura e umidade
#define TRIG_PIN 5     // HC-SR04: Trigger do sensor ultrassônico
#define ECHO_PIN 18    // HC-SR04: Echo do sensor ultrassônico
#define PIR_PIN 19     // PIR: Sensor de movimento
#define LDR_PIN 34     // LDR: Sensor de luminosidade (ADC)
#define BUZZER_PIN 4   // Buzzer para alarme

// I2C Pins
#define SDA_PIN 21     // Serial Data
#define SCL_PIN 23     // Serial Clock

//=====================================
// Constants for Flood Detection
//=====================================
#define DHT_TYPE DHT22              // Modelo do sensor DHT
#define WATER_CRITICAL_LEVEL 15.0   // Nível crítico de água (cm) - EVACUAÇÃO
#define WATER_ALERT_LEVEL 30.0      // Nível de alerta de água (cm) - ATENÇÃO
#define HUMIDITY_CRITICAL 90.0      // Umidade crítica (%) - Indica chuva intensa
#define TEMP_ANOMALY 35.0           // Temperatura anômala (°C)
#define LIGHT_STORM_THRESHOLD 10.0  // Threshold de luz (%) - Escurecimento súbito

//=====================================
// Alert Levels
//=====================================
enum AlertLevel {
    NORMAL = 0,     // Situação normal
    ATTENTION = 1,  // Atenção - monitorar
    CRITICAL = 2    // Crítico - evacuação
};

//=====================================
// Global Instances
//=====================================
static DHT dht(DHT_PIN, DHT_TYPE);
static LiquidCrystal_I2C lcd(0x27, 16, 2);

//=====================================
// System State
//=====================================
static AlertLevel currentAlertLevel = NORMAL;
static bool isAlarmActive = false;
static unsigned long lastAlarmTrigger = 0;
static unsigned long lastDataSave = 0;
static const unsigned long ALARM_COOLDOWN = 10000;  // 10 segundos entre alarmes
static const unsigned long DATA_SAVE_INTERVAL = 30000; // 30 segundos entre salvamentos
static int fileCounter = 0;

// Device ID único
static const String DEVICE_ID = "flood_monitor_01";

//=====================================
// Data Storage Functions
//=====================================
bool initDataStorage() {
    #if DEV_MODE
        Serial.println("=== MODO DESENVOLVIMENTO ===");
        Serial.println("Dados serão exibidos no Serial Monitor");
        return true;
    #else
        if (!SPIFFS.begin(true)) {
            Serial.println("ERRO: Falha ao inicializar SPIFFS!");
            return false;
        }
        
        size_t totalBytes = SPIFFS.totalBytes();
        size_t usedBytes = SPIFFS.usedBytes();
        
        Serial.println("=== SPIFFS Inicializado ===");
        Serial.printf("Total: %d bytes\n", totalBytes);
        Serial.printf("Usado: %d bytes\n", usedBytes);
        Serial.printf("Livre: %d bytes\n", totalBytes - usedBytes);
        
        return true;
    #endif
}

void cleanupOldFiles() {
    #if !DEV_MODE
        // Manter apenas os últimos 50 arquivos para não esgotar o espaço
        File root = SPIFFS.open("/");
        File file = root.openNextFile();
        int fileCount = 0;
        
        while (file) {
            if (String(file.name()).startsWith("/data_")) {
                fileCount++;
            }
            file = root.openNextFile();
        }
        
        if (fileCount > 50) {
            Serial.printf("Limpando arquivos antigos... (%d arquivos)\n", fileCount);
            // Implementar lógica de limpeza se necessário
        }
    #else
        Serial.println("Limpeza de arquivos não necessária no modo DEV");
    #endif
}

//=====================================
// Sensor Reading Functions
//=====================================
float readUltrasonic() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    long duration = pulseIn(ECHO_PIN, HIGH, 30000); // Timeout de 30ms
    if (duration == 0) {
        return -1; // Erro na leitura
    }
    
    return duration * 0.034 / 2;
}

bool readPIR() {
    return digitalRead(PIR_PIN);
}

float readLDR() {
    int ldrValue = analogRead(LDR_PIN);
    return (ldrValue / 4095.0) * 100;
}

//=====================================
// Flood Detection Logic
//=====================================
AlertLevel analyzeFloodRisk(float waterDistance, float humidity, float temperature, float lightLevel, bool motionDetected) {
    // Condições críticas (EVACUAÇÃO IMEDIATA)
    if (waterDistance > 0 && waterDistance <= WATER_CRITICAL_LEVEL) {
        Serial.println("CRÍTICO: Água muito próxima!");
        return CRITICAL;
    }
    
    if (humidity >= HUMIDITY_CRITICAL && lightLevel <= LIGHT_STORM_THRESHOLD) {
        Serial.println("CRÍTICO: Tempestade intensa detectada!");
        return CRITICAL;
    }
    
    // Condições de atenção
    if (waterDistance > 0 && waterDistance <= WATER_ALERT_LEVEL) {
        Serial.println("ATENÇÃO: Nível de água elevado!");
        return ATTENTION;
    }
    
    if (humidity >= 85.0) {
        Serial.println("ATENÇÃO: Umidade muito alta!");
        return ATTENTION;
    }
    
    if (lightLevel <= LIGHT_STORM_THRESHOLD) {
        Serial.println("ATENÇÃO: Escurecimento súbito detectado!");
        return ATTENTION;
    }
    
    if (temperature >= TEMP_ANOMALY) {
        Serial.println("ATENÇÃO: Temperatura anômala!");
        return ATTENTION;
    }
    
    return NORMAL;
}

//=====================================
// Alert System
//=====================================
void soundAlertPattern(AlertLevel level) {
    switch(level) {
        case NORMAL:
            // Sem som
            break;
            
        case ATTENTION:
            // 2 beeps curtos
            for (int i = 0; i < 2; i++) {
                tone(BUZZER_PIN, 1000);
                delay(200);
                noTone(BUZZER_PIN);
                delay(200);
            }
            break;
            
        case CRITICAL:
            // Sirene contínua
            for (int i = 0; i < 5; i++) {
                tone(BUZZER_PIN, 2000);
                delay(300);
                tone(BUZZER_PIN, 1500);
                delay(300);
            }
            noTone(BUZZER_PIN);
            break;
    }
}

void updateLCD(float temp, float hum, float waterDist, AlertLevel alertLevel) {
    lcd.clear();
    
    // Linha 1: Dados principais
    lcd.setCursor(0, 0);
    if (isnan(temp) || isnan(hum)) {
        lcd.print("Sensor Error!");
    } else {
        lcd.printf("T:%.1fC H:%.0f%%", temp, hum);
    }
    
    // Linha 2: Status do alerta
    lcd.setCursor(0, 1);
    switch(alertLevel) {
        case NORMAL:
            if (waterDist > 0) {
                lcd.printf("Normal %.0fcm", waterDist);
            } else {
                lcd.print("Sistema Normal");
            }
            break;
        case ATTENTION:
            lcd.print("ATENCAO!");
            break;
        case CRITICAL:
            lcd.print("EVACUACAO!");
            break;
    }
}

//=====================================
// Data Logging
//=====================================
bool saveDataToFile(float temp, float hum, float waterDist, float lightLevel, bool motion, AlertLevel alertLevel) {
    // Criar JSON com dados dos sensores
    DynamicJsonDocument doc(1024);
    
    doc["device_id"] = DEVICE_ID;
    doc["timestamp"] = millis();
    doc["datetime"] = String(millis()); // Timestamp simples
    
    // Dados dos sensores
    doc["sensors"]["temperature"] = temp;
    doc["sensors"]["humidity"] = hum;
    doc["sensors"]["water_distance"] = waterDist;
    doc["sensors"]["light_level"] = lightLevel;
    doc["sensors"]["motion_detected"] = motion;
    
    // Status do sistema
    doc["status"]["alert_level"] = alertLevel;
    doc["status"]["alert_name"] = (alertLevel == NORMAL) ? "NORMAL" : 
                                  (alertLevel == ATTENTION) ? "ATTENTION" : "CRITICAL";
    
    // Análise de risco
    doc["analysis"]["flood_risk"] = (alertLevel >= ATTENTION);
    doc["analysis"]["evacuation_needed"] = (alertLevel == CRITICAL);
    
    #if DEV_MODE
        // Modo desenvolvimento - mostrar JSON no Serial
        Serial.println("\n=== DADOS DE SENSORES (DEV MODE) ===");
        Serial.printf("Timestamp: %lu\n", millis());
        Serial.println("JSON:");
        serializeJsonPretty(doc, Serial);
        Serial.println("\n=== FIM DOS DADOS ===");
        fileCounter++;
        return true;
    #else
        // Modo produção - salvar em SPIFFS
        String filename = "/data_" + String(millis()) + ".json";
        
        File file = SPIFFS.open(filename, "w");
        if (!file) {
            Serial.println("ERRO: Falha ao criar arquivo!");
            return false;
        }
        
        if (serializeJson(doc, file) == 0) {
            Serial.println("ERRO: Falha ao escrever JSON!");
            file.close();
            return false;
        }
        
        file.close();
        fileCounter++;
        
        Serial.printf("Dados salvos: %s (%d arquivos)\n", filename.c_str(), fileCounter);
        return true;
    #endif
}

//=====================================
// Serial Commands
//=====================================
void processSerialCommands() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        
        #if DEV_MODE
            if (command == "STATUS") {
                Serial.println("=== STATUS DO SISTEMA (DEV MODE) ===");
                Serial.printf("Device ID: %s\n", DEVICE_ID.c_str());
                Serial.printf("Uptime: %lu ms\n", millis());
                Serial.printf("Alert Level: %s\n", 
                    (currentAlertLevel == NORMAL) ? "NORMAL" : 
                    (currentAlertLevel == ATTENTION) ? "ATTENTION" : "CRITICAL");
                Serial.printf("Dados coletados: %d\n", fileCounter);
                Serial.println("Modo: DESENVOLVIMENTO (dados no Serial)");
            } else {
                Serial.println("=== COMANDOS DISPONÍVEIS (DEV MODE) ===");
                Serial.println("  STATUS - status do sistema");
                Serial.println("Outros comandos disponíveis apenas no modo PRODUÇÃO");
            }
        #else
            if (command == "LIST") {
                Serial.println("=== ARQUIVOS DISPONÍVEIS ===");
                File root = SPIFFS.open("/");
                File file = root.openNextFile();
                int count = 0;
                
                while (file) {
                    if (String(file.name()).startsWith("/data_")) {
                        Serial.printf("%s (%d bytes)\n", file.name(), file.size());
                        count++;
                    }
                    file = root.openNextFile();
                }
                Serial.printf("Total: %d arquivos\n", count);
                
            } else if (command.startsWith("GET ")) {
                String filename = command.substring(4);
                if (!filename.startsWith("/")) {
                    filename = "/" + filename;
                }
                
                File file = SPIFFS.open(filename, "r");
                if (file) {
                    Serial.printf("=== CONTEÚDO: %s ===\n", filename.c_str());
                    while (file.available()) {
                        Serial.write(file.read());
                    }
                    Serial.println("\n=== FIM DO ARQUIVO ===");
                    file.close();
                } else {
                    Serial.printf("ERRO: Arquivo não encontrado: %s\n", filename.c_str());
                }
                
            } else if (command.startsWith("DELETE ")) {
                String filename = command.substring(7);
                if (!filename.startsWith("/")) {
                    filename = "/" + filename;
                }
                
                if (SPIFFS.remove(filename)) {
                    Serial.printf("Arquivo removido: %s\n", filename.c_str());
                    fileCounter--;
                } else {
                    Serial.printf("ERRO: Falha ao remover: %s\n", filename.c_str());
                }
                
            } else if (command == "STATUS") {
                size_t total = SPIFFS.totalBytes();
                size_t used = SPIFFS.usedBytes();
                
                Serial.println("=== STATUS DO SISTEMA ===");
                Serial.printf("Device ID: %s\n", DEVICE_ID.c_str());
                Serial.printf("Uptime: %lu ms\n", millis());
                Serial.printf("Alert Level: %s\n", 
                    (currentAlertLevel == NORMAL) ? "NORMAL" : 
                    (currentAlertLevel == ATTENTION) ? "ATTENTION" : "CRITICAL");
                Serial.printf("Arquivos: %d\n", fileCounter);
                Serial.printf("SPIFFS: %d/%d bytes (%.1f%%)\n", used, total, (used * 100.0) / total);
                
            } else {
                Serial.println("Comandos disponíveis:");
                Serial.println("  LIST - listar arquivos");
                Serial.println("  GET <filename> - ler arquivo");
                Serial.println("  DELETE <filename> - remover arquivo");
                Serial.println("  STATUS - status do sistema");
            }
        #endif
    }
}

//=====================================
// I2C and LCD Initialization
//=====================================
void initI2C() {
    Wire.begin(SDA_PIN, SCL_PIN);
    delay(100);
    
    lcd.init();
    lcd.backlight();
    lcd.clear();
    lcd.print("Flood Monitor");
    lcd.setCursor(0, 1);
    lcd.print("Iniciando...");
    
    Serial.println("LCD inicializado!");
}

//=====================================
// Setup Function
//=====================================
void setup() {
    Serial.begin(115200);
    Serial.println("\n=== SISTEMA DE MONITORAMENTO DE ENCHENTES ===");
    Serial.println("Global Solution 2025 - FIAP");
    
    // Inicializar componentes
    initI2C();
    dht.begin();
    
    // Configurar pinos
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(PIR_PIN, INPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    
    // Inicializar sistema de dados
    initDataStorage();
    cleanupOldFiles();
    
    // Aguardar estabilização
    Serial.println("Aguardando estabilização dos sensores...");
    delay(3000);
    
    lcd.clear();
    lcd.print("Sistema Pronto!");
    Serial.println("=== SISTEMA INICIALIZADO ===");
    Serial.println("Comandos: LIST, GET, DELETE, STATUS");
}

//=====================================
// Main Loop
//=====================================
void loop() {
    unsigned long currentMillis = millis();
    
    // Processar comandos serial
    processSerialCommands();
    
    // Ler sensores
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    float waterDistance = readUltrasonic();
    bool motionDetected = readPIR();
    float lightLevel = readLDR();
    
    // Validar leituras
    if (isnan(humidity) || isnan(temperature)) {
        Serial.println("ERRO: Falha na leitura do DHT22!");
        delay(2000);
        return;
    }
    
    // Analisar risco de enchente
    AlertLevel newAlertLevel = analyzeFloodRisk(waterDistance, humidity, temperature, lightLevel, motionDetected);
    
    // Verificar mudança de nível de alerta
    if (newAlertLevel != currentAlertLevel) {
        currentAlertLevel = newAlertLevel;
        Serial.printf("MUDANÇA DE ALERTA: %s\n", 
            (currentAlertLevel == NORMAL) ? "NORMAL" : 
            (currentAlertLevel == ATTENTION) ? "ATENÇÃO" : "CRÍTICO");
        
        // Ativar alarme sonoro
        if (currentAlertLevel > NORMAL && 
            (currentMillis - lastAlarmTrigger > ALARM_COOLDOWN)) {
            soundAlertPattern(currentAlertLevel);
            lastAlarmTrigger = currentMillis;
        }
    }
    
    // Atualizar display
    updateLCD(temperature, humidity, waterDistance, currentAlertLevel);
    
    // Salvar dados periodicamente
    if (currentMillis - lastDataSave >= DATA_SAVE_INTERVAL) {
        if (saveDataToFile(temperature, humidity, waterDistance, lightLevel, motionDetected, currentAlertLevel)) {
            Serial.println("Dados salvos com sucesso!");
        }
        lastDataSave = currentMillis;
    }
    
    // Log periódico no Serial
    if (currentMillis % 5000 < 100) { // A cada 5 segundos
        Serial.println("\n=== LEITURAS DOS SENSORES ===");
        Serial.printf("Temperatura: %.2f°C\n", temperature);
        Serial.printf("Umidade: %.2f%%\n", humidity);
        Serial.printf("Distância Água: %.2f cm\n", waterDistance);
        Serial.printf("Luminosidade: %.2f%%\n", lightLevel);
        Serial.printf("Movimento: %s\n", motionDetected ? "SIM" : "NÃO");
        Serial.printf("Nível de Alerta: %s\n", 
            (currentAlertLevel == NORMAL) ? "NORMAL" : 
            (currentAlertLevel == ATTENTION) ? "ATENÇÃO" : "CRÍTICO");
    }
    
    delay(1000); // Loop a cada 1 segundo
}
