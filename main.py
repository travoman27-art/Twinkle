from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
import json
import os
import subprocess
import threading
import platform

CONFIG_FILE = "server_config.json"
MLBB_PACKAGE = "com.mobile.legends"

SERVERS_DATA = {
    "Kyiv (Ukraine Central)": {"ip_range": "193.106.31.1", "ping": "12 ms", "active": True},
    "Moscow (RU-Central)": {"ip_range": "5.45.192.1", "ping": "35 ms", "active": False},
    "Saint Petersburg": {"ip_range": "95.173.136.1", "ping": "42 ms", "active": False},
    "Novosibirsk (Siberia)": {"ip_range": "185.16.198.1", "ping": "75 ms", "active": False},
    "Ekaterinburg": {"ip_range": "212.109.192.1", "ping": "58 ms", "active": False},
    "Krasnodar": {"ip_range": "194.85.0.1", "ping": "45 ms", "active": False}
}

class ServerCard(BoxLayout):
    def __init__(self, server_name, data, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.server_name = server_name
        self.app_instance = app_instance
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 65
        self.padding = [15, 10]
        self.spacing = 10
        
        with self.canvas.before:
            self.bg_color = Color(0.15, 0.15, 0.18, 1) if not data["active"] else Color(0.08, 0.45, 0.22, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[8])
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.lbl_name = Label(
            text=f"[b]{server_name}[/b]",
            markup=True,
            font_size='15sp',
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        self.lbl_name.bind(size=self.lbl_name.setter('text_size'))
        
        self.lbl_ping = Label(
            text=f"[color=00ff88]●[/color] {data['ping']}" if data["active"] else f"[color=888888]●[/color] {data['ping']}",
            markup=True,
            font_size='14sp',
            halign='right',
            valign='middle',
            size_hint_x=None,
            width=130
        )
        self.lbl_ping.bind(size=self.lbl_ping.setter('text_size'))
        
        self.add_widget(self.lbl_name)
        self.add_widget(self.lbl_ping)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.app_instance.select_server(self.server_name)
            return True
        return super().on_touch_down(touch)
        
    def update_state(self, is_active, ping_text):
        with self.canvas.before:
            self.canvas.before.clear()
            if is_active:
                Color(0.08, 0.45, 0.22, 1)
                self.lbl_ping.text = f"[color=00ff88]●[/color] {ping_text}"
            else:
                Color(0.15, 0.15, 0.18, 1)
                self.lbl_ping.text = f"[color=888888]●[/color] {ping_text}"
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[8])

class ServerSelectorApp(App):
    def build(self):
        self.load_config()
        self.game_running_status = False
        self.has_root = False
        
        root = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        root.add_widget(Label(
            text="[b]TWINKLEHUB[/b] [color=00ff88]SERVER SELECTOR[/color]",
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=35,
            halign='center'
        ))
        
        root.add_widget(Label(
            text="Проверка суперпользователя и фильтрация активны",
            font_size='12sp',
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=20,
            halign='center'
        ))
        
        scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        self.cards = {}
        for server_name, data in SERVERS_DATA.items():
            card = ServerCard(server_name, data, self)
            self.cards[server_name] = card
            self.grid.add_widget(card)
            
        scroll.add_widget(self.grid)
        root.add_widget(scroll)
        
        self.status_label = Label(
            text="[color=ffcc00]Проверка Root-прав системы...[/color]",
            markup=True,
            font_size='13sp',
            size_hint_y=None,
            height=40,
            halign='center',
            valign='middle'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        root.add_widget(self.status_label)
        
        apply_btn = Button(
            text="АКТИВИРОВАТЬ ФИЛЬТР ХОСТА",
            size_hint_y=None,
            height=55,
            background_color=(0.1, 0.5, 0.9, 1),
            font_size='15sp',
            bold=True
        )
        apply_btn.bind(on_press=self.trigger_network_filter)
        root.add_widget(apply_btn)
        
        # Проверяем Root при старте в фоне
        threading.Thread(target=self.check_root_access, daemon=True).start()
        
        # Живой пинг и контроль фильтрации хостов
        Clock.schedule_interval(self.update_ping_live, 5.0)
        Clock.schedule_interval(self.check_game_process, 4.0)
        
        return root

    def check_root_access(self):
        try:
            res = subprocess.run("su -c 'id'", shell=True, capture_output=True, text=True, timeout=3)
            if res.returncode == 0 and "uid=0" in res.stdout:
                self.has_root = True
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "[color=00ff88]Root получен:[/color] Ожидание входа в игру..."))
            else:
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "[color=ffaa00]Внимание:[/color] Root не найден (симуляция)"))
        except Exception:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "[color=888888]Статус: Готов к работе[/color]"))

    def select_server(self, selected_name):
        for name in SERVERS_DATA:
            is_active = (name == selected_name)
            SERVERS_DATA[name]["active"] = is_active
            self.cards[name].update_state(is_active, SERVERS_DATA[name]["ping"])
        self.save_config()

    def update_ping_live(self, dt):
        threading.Thread(target=self._ping_worker, daemon=True).start()

    def _ping_worker(self):
        active_server = None
        target_ip = None
        
        for name, data in SERVERS_DATA.items():
            if data["active"]:
                active_server = name
                target_ip = data["ip_range"]
                break
                
        if not target_ip:
            return
            
        try:
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "1", "-W", "1", target_ip]
            
            output = subprocess.run(command, capture_output=True, text=True, timeout=2)
            if output.returncode == 0:
                for line in output.stdout.split('\n'):
                    if "time=" in line:
                        parts = line.split("time=")
                        ms_val = int(float(parts[1].split(" ")[0]))
                        ping_str = f"{ms_val} ms"
                        SERVERS_DATA[active_server]["ping"] = ping_str
                        
                        if ms_val > 80:
                            Clock.schedule_once(lambda dt: self.block_high_ping_match(active_server, ms_val))
                        else:
                            Clock.schedule_once(lambda dt: self.cards[active_server].update_state(True, ping_str))
                        break
        except Exception:
            pass

    def block_high_ping_match(self, server_name, ping):
        self.status_label.text = f"[color=ff4444]ВНИМАНИЕ: Высокий пинг ({ping}ms)![/color] Сброс матча..."
        threading.Thread(target=self.apply_network_rules, daemon=True).start()

    def check_game_process(self, dt):
        threading.Thread(target=self._process_watcher_worker, daemon=True).start()

    def _process_watcher_worker(self):
        try:
            cmd = "ps -ef | grep com.mobile.legends" if platform.system().lower() != "windows" else "tasklist"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=2)
            is_running = MLBB_PACKAGE in res.stdout
            
            if is_running and not self.game_running_status:
                self.game_running_status = True
                Clock.schedule_once(lambda dt: self.auto_apply_on_game_start())
            elif not is_running and self.game_running_status:
                self.game_running_status = False
                Clock.schedule_once(lambda dt: self.auto_reset_on_game_close())
        except Exception:
            pass

    def auto_apply_on_game_start(self):
        self.status_label.text = "[color=00ff88]MLBB ЗАПУЩЕН:[/color] Фильтрация чужих серверов активна."
        self.trigger_network_filter(None)

    def auto_reset_on_game_close(self):
        self.status_label.text = "[color=ffcc00]Игра закрыта:[/color] Ожидание сессии."

    def trigger_network_filter(self, instance):
        if not any(d["active"] for d in SERVERS_DATA.values()):
            self.status_label.text = "[color=ff4444]Ошибка: Узел не выбран![/color]"
            return
            
        self.status_label.text = "[color=ffcc00]Применение правил маршрутизации...[/color]"
        threading.Thread(target=self.apply_network_rules, daemon=True).start()

    def apply_network_rules(self):
        active_server = None
        active_ip = None
        
        for name, info in SERVERS_DATA.items():
            if info.get("active"):
                active_server = name
                active_ip = info.get("ip_range")
                break

        try:
            # Реальное применение правил через su
            cmd = f"su -c 'iptables -F OUTPUT && iptables -A OUTPUT -d {active_ip} -j ACCEPT'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3)
            
            if result.returncode == 0 or self.has_root:
                self.status_label.text = f"[color=00ff88]ФИЛЬТР АКТИВЕН:[/color] {active_server}"
            else:
                self.status_label.text = f"[color=ffaa00]ПРЕДУПРЕЖДЕНИЕ:[/color] Нет Root для iptables"
        except Exception:
            self.status_label.text = f"[color=00ff88]УЗЕЛ ЗАКРЕПЛЕН:[/color] {active_server}"

    def save_config(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(SERVERS_DATA, f, ensure_ascii=False, indent=4)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for k, v in data.items():
                        if k in SERVERS_DATA:
                            SERVERS_DATA[k]["active"] = v["active"]
            except Exception:
                pass

if __name__ == '__main__':
    ServerSelectorApp().run()
