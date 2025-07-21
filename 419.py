import google.generativeai as genai

# API
genai.configure(api_key="YOUR_API_KEY") # Paste your own API.

# LogicalAgent class
class LogicalAgent:
    def __init__(self):
        self.facts = set()
        self.rules = dict()

    def tell_fact(self, fact):
        print(f"[FACT] {fact}")
        self.facts.add(fact)

    def tell_rule(self, rule):
        condition, action = rule.split("->")
        condition = condition.strip()
        action = action.strip()
        if condition in self.rules:
            self.rules[condition].append(action)
        else:
            self.rules[condition] = [action]
        print(f"[RULE] {condition} -> {action}")

    def infer(self):
        triggered_actions = []
        for condition, actions in self.rules.items():
            if condition in self.facts:
                triggered_actions.extend(actions)
        return triggered_actions

    def reset(self):
        self.facts.clear()

# Gemini ile LLM tabanlı fakt çıkarıcı
def llm_fact_extractor(command):
    prompt = f"""
Aşağıdaki kullanıcı komutu yazım hatalı, kısaltmalı, argo olabilir.
Bu komutu temsil eden tek kelimelik bir mantıksal fakt üret (örneğin: cold_weather, turn_on_tv).

Örnekler:
"üşüyorum" -> cold_weather
"üşüyom" -> cold_weather
"film izlyom" -> watching_movie
"film izliyorum" -> watching_movie
"tv yi aça" -> turn_on_tv
"klimy aç" -> turn_on_heater
"ışık aç" -> turn_on_lamps
"kapıya biri geldi" -> someone_at_door
"ev boşş" -> no_one_home
"ısıyı artır" -> increase_temperature
"ısıyı düşür" -> decrease_temperature
"ışığı kapat" -> turn_off_light
"tv yi kapat" -> turn_off_tv
"klimayı kapat" -> turn_off_heater
"perdeleri aç" -> open_curtains
"perdeleri kapat" -> close_curtains
"kapıyı kapat" -> close_door
"kapıyı aç" -> open_door
"kapıyı kilitle" -> lock_door
"kapı kilidini aç" -> unlock_door
"alarmı kur" -> set_alarm
"alarm kapalı" -> alarm_off
"müziği aç" -> play_music
"müziği durdur" -> stop_music
"sesini aç" -> increase_volume
"sesini kıs" -> decrease_volume
"fanı aç" -> turn_on_fan
"fanı kapat" -> turn_off_fan
"pencereyi aç" -> open_window
"pencereyi kapat" -> close_window

# İkili eylemler
"gece oldu" -> night_time
"sabah oldu" -> morning_time
"film izliyorum" -> watching_movie
"yatak zamanı" -> bedtime
"eve geldim" -> arrived_home
"hava çok sıcak" -> hot_weather

Komut: "{command}"
Mantıksal fakt:
"""
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[HATA] Gemini isteği başarısız: {e}")
        return None

agent = LogicalAgent()

# KURALLAR

# sıcak - soğuk hava
agent.tell_rule("cold_weather -> turn_on_heater")
agent.tell_rule("hot_weather -> turn_on_airconditioner")

# gece olduysa hem ışık aç hem perdeyi kapat
agent.tell_rule("night_time -> turn_on_lamps")
agent.tell_rule("night_time -> close_curtains")

# sabah olduysa perde aç ve ışığı kapat
agent.tell_rule("morning_time -> open_curtains")
agent.tell_rule("morning_time -> turn_off_light")

# diğer kurallar
agent.tell_rule("no_one_home -> turn_off_tv")
agent.tell_rule("open_door -> door_is_opened")
agent.tell_rule("someone_at_door -> open_door")
agent.tell_rule("turn_on_tv -> tv_power_on")
agent.tell_rule("close_curtains -> curtains_closed")
agent.tell_rule("increase_temperature -> raise_heater_temp")

# kapatma komutları
agent.tell_rule("decrease_temperature -> lower_heater_temp")
agent.tell_rule("turn_off_light -> lights_off")
agent.tell_rule("turn_off_tv -> tv_power_off")
agent.tell_rule("turn_off_heater -> heater_power_off")
agent.tell_rule("open_curtains -> curtains_open")
agent.tell_rule("close_door -> door_closed")

# kapıyı kilitleme ve kilit açma
agent.tell_rule("lock_door -> door_locked")
agent.tell_rule("unlock_door -> door_unlocked")

# alarm kurma ve kapatma
agent.tell_rule("set_alarm -> alarm_activated")
agent.tell_rule("alarm_off -> alarm_deactivated")

# müzik açma ve kapatma
agent.tell_rule("play_music -> music_playing")
agent.tell_rule("stop_music -> music_stopped")

# ses yüksetlme ve kısma
agent.tell_rule("increase_volume -> volume_up")
agent.tell_rule("decrease_volume -> volume_down")

# fan açma ve kapatma
agent.tell_rule("turn_on_fan -> fan_on")
agent.tell_rule("turn_off_fan -> fan_off")

# pencere açma ve kapatma
agent.tell_rule("open_window -> window_open")
agent.tell_rule("close_window -> window_closed")

# ikili eylem kuralları
agent.tell_rule("play_movie -> dim_lights")
agent.tell_rule("play_movie -> close_curtains")

agent.tell_rule("bedtime -> turn_off_light")
agent.tell_rule("bedtime -> set_alarm")

agent.tell_rule("arrived_home -> open_door")
agent.tell_rule("arrived_home -> turn_on_lamps")
agent.tell_rule("arrived_home -> play_music")

# terminalden komut alma
print("\n=== GEMINI SMART HOME SYSTEM ===")
print("Komut girin (çıkmak için 'çık' veya 'durdur' yazın):\n")

while True:
    cmd = input(">> Komut: ").strip()
    if cmd.lower() in ["çık", "exit", "quit", "durdur"]:
        print("Program durduruldu. Çıkılıyor...")
        break

    agent.reset()

    fact = llm_fact_extractor(cmd)
    if fact:
        agent.tell_fact(fact)
        actions = agent.infer()
        if actions:
            print("\n[ETKİLENEN EYLEMLER]:")
            for act in actions:
                print(f"-> {act}")
        else:
            print("[!] Bu fakta karşılık gelen bir kural bulunamadı.")
    else:
        print("[!] Fact çıkarılamadı. Lütfen farklı bir komut deneyin.")
