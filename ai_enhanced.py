# 增强版变速圆周运动小球动画实验
from vpython import *
import math
import time
import csv
from datetime import datetime

# 全局变量
balls = []  # 小球列表
data_records = []  # 数据记录
recording = False  # 是否记录数据
start_time = 0
current_ball_index = 0  # 当前选中的小球索引

class PhysicsBall:
    def __init__(self, mass=0.1, radius=2.0, ball_radius=0.1, color_val=color.red, 
                 initial_theta=0.5, initial_omega=0, name="小球1"):
        self.mass = mass
        self.radius = radius
        self.ball_radius = ball_radius
        self.theta = initial_theta
        self.omega = initial_omega
        self.name = name
        self.g = 9.8  # 重力加速度
        
        # 创建可视化对象
        self.ball = sphere(pos=self.get_position(), radius=ball_radius, 
                          color=color_val, make_trail=True, trail_type="curve", 
                          interval=10, retain=300)
        self.arrow_v = arrow(pos=self.ball.pos, axis=vector(0,0,0), 
                            color=color.blue, shaftwidth=0.03)
        self.arrow_c = arrow(pos=self.ball.pos, axis=vector(0,0,0), 
                            color=color.green, shaftwidth=0.03)
        self.arrow_g = arrow(pos=self.ball.pos, axis=vector(0,0,0), 
                            color=color.orange, shaftwidth=0.03)
        
        # 物理量
        self.kinetic_energy = 0
        self.potential_energy = 0
        self.total_energy = 0
        self.speed = 0
        self.centripetal_acc = 0
        
    def get_position(self):
        x = self.radius * sin(self.theta)
        y = self.radius * cos(self.theta)
        return vector(x, y, 0)
    
    def update(self, dt):
        # 重力在切向的分量产生的角加速度
        tangential_acc = self.g * sin(self.theta)
        alpha = tangential_acc / self.radius
        
        # 更新角速度和角度
        self.omega += alpha * dt
        self.theta += self.omega * dt
        
        # 更新位置
        self.ball.pos = self.get_position()
        
        # 计算物理量
        self.speed = abs(self.omega * self.radius)
        self.kinetic_energy = 0.5 * self.mass * self.speed**2
        height = self.radius * cos(self.theta) + self.radius  # 相对于最低点的高度
        self.potential_energy = self.mass * self.g * height
        self.total_energy = self.kinetic_energy + self.potential_energy
        self.centripetal_acc = self.omega**2 * self.radius
        
        # 更新箭头
        self.update_arrows()
    
    def update_arrows(self):
        # 速度箭头（切向）
        v = self.omega * self.radius
        vx = v * cos(self.theta)
        vy = -v * sin(self.theta)  # 负号因为角度定义
        self.arrow_v.pos = self.ball.pos
        self.arrow_v.axis = vector(vx, vy, 0) * 0.15
        
        # 向心力箭头（指向圆心）
        centripetal_force = self.mass * self.centripetal_acc
        force_scale = 0.05
        self.arrow_c.pos = self.ball.pos
        center_dir = -self.ball.pos.norm()
        self.arrow_c.axis = center_dir * centripetal_force * force_scale
        
        # 重力箭头
        gravity_force = self.mass * self.g
        self.arrow_g.pos = self.ball.pos
        self.arrow_g.axis = vector(0, -gravity_force * force_scale, 0)
    
    def reset(self, theta, omega):
        self.theta = theta
        self.omega = omega
        self.ball.pos = self.get_position()
        self.ball.clear_trail()
        self.update_arrows()

# 场景设置
scene = canvas(title="增强版变速圆周运动小球实验", width=1200, height=800, background=color.white)
scene.camera.pos = vector(0, 0, 8)

# 绘制圆轨道
circle = ring(pos=vector(0,0,0), axis=vector(0,0,1), radius=2.0, thickness=0.02, color=color.gray(0.7))

# 创建坐标轴
axis_x = arrow(pos=vector(-3,0,0), axis=vector(6,0,0), color=color.gray(0.5), shaftwidth=0.01)
axis_y = arrow(pos=vector(0,-3,0), axis=vector(0,6,0), color=color.gray(0.5), shaftwidth=0.01)

# 添加刻度标记
for i in range(-2, 3):
    if i != 0:
        # X轴刻度
        box(pos=vector(i, 0, 0), size=vector(0.02, 0.1, 0.02), color=color.gray(0.5))
        label(pos=vector(i, -0.2, 0), text=str(i), height=10, color=color.black, box=False)
        # Y轴刻度
        box(pos=vector(0, i, 0), size=vector(0.1, 0.02, 0.02), color=color.gray(0.5))
        label(pos=vector(-0.2, i, 0), text=str(i), height=10, color=color.black, box=False)

# 状态变量
is_running = False
show_energy_graph = True
show_vectors = True

# 创建初始小球
ball1 = PhysicsBall(mass=0.1, radius=2.0, ball_radius=0.08, color_val=color.red, 
                   initial_theta=0.5, initial_omega=0, name="小球1")
ball2 = PhysicsBall(mass=0.15, radius=2.0, ball_radius=0.08, color_val=color.blue, 
                   initial_theta=1.0, initial_omega=0, name="小球2")
ball3 = PhysicsBall(mass=0.2, radius=2.0, ball_radius=0.08, color_val=color.green, 
                   initial_theta=-0.5, initial_omega=0, name="小球3")

balls = [ball1, ball2, ball3]

# 图表设置
if show_energy_graph:
    energy_graph = graph(title="能量随时间变化", xtitle="时间 (s)", ytitle="能量 (J)", 
                        width=400, height=200, align="left")
    ke_curve = gcurve(graph=energy_graph, color=color.red, label="动能")
    pe_curve = gcurve(graph=energy_graph, color=color.blue, label="势能") 
    te_curve = gcurve(graph=energy_graph, color=color.green, label="总能量")

# 控件回调函数
def set_theta(s):
    global current_ball_index
    if not is_running and current_ball_index < len(balls):
        balls[current_ball_index].reset(s.value, balls[current_ball_index].omega)

def set_omega(s):
    global current_ball_index
    if not is_running and current_ball_index < len(balls):
        balls[current_ball_index].omega = s.value
        balls[current_ball_index].update_arrows()

def set_mass(s):
    global current_ball_index
    if not is_running and current_ball_index < len(balls):
        balls[current_ball_index].mass = s.value

def set_gravity(s):
    for ball in balls:
        ball.g = s.value

def toggle_run():
    global is_running, start_time, recording
    is_running = not is_running
    if is_running:
        btn_run.text = "暂停"
        start_time = time.time()
    else:
        btn_run.text = "开始"

def reset_all():
    global is_running, data_records
    is_running = False
    btn_run.text = "开始"
    for i, ball in enumerate(balls):
        ball.reset(slider_theta.value if i == current_ball_index else ball.theta, 
                  slider_omega.value if i == current_ball_index else ball.omega)
    data_records = []
    if show_energy_graph:
        ke_curve.data = []
        pe_curve.data = []
        te_curve.data = []

def toggle_recording():
    global recording, data_records
    recording = not recording
    if recording:
        btn_record.text = "停止记录"
        data_records = []
    else:
        btn_record.text = "开始记录"

def export_data():
    if data_records:
        filename = f"physics_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['时间(s)', '小球', '角度(rad)', '角速度(rad/s)', '速度(m/s)', 
                           '动能(J)', '势能(J)', '总能量(J)', '向心加速度(m/s²)'])
            writer.writerows(data_records)
        print(f"数据已导出到 {filename}")

def switch_ball():
    global current_ball_index
    current_ball_index = (current_ball_index + 1) % len(balls)
    current_ball = balls[current_ball_index]
    slider_theta.value = current_ball.theta
    slider_omega.value = current_ball.omega
    slider_mass.value = current_ball.mass
    label_current_ball.text = f"当前小球: {current_ball.name}"

def toggle_vectors():
    global show_vectors
    show_vectors = not show_vectors
    for ball in balls:
        ball.arrow_v.visible = show_vectors
        ball.arrow_c.visible = show_vectors
        ball.arrow_g.visible = show_vectors

def toggle_ball_visibility(ball_index):
    balls[ball_index].ball.visible = not balls[ball_index].ball.visible
    balls[ball_index].arrow_v.visible = balls[ball_index].ball.visible and show_vectors
    balls[ball_index].arrow_c.visible = balls[ball_index].ball.visible and show_vectors
    balls[ball_index].arrow_g.visible = balls[ball_index].ball.visible and show_vectors

# 控制面板
scene.append_to_caption("\n<b>控制面板</b>\n")

# 当前小球选择
scene.append_to_caption("当前小球: ")
label_current_ball = wtext(text=f"当前小球: {balls[0].name}")
scene.append_to_caption("    ")
button(text="切换小球", bind=switch_ball)
scene.append_to_caption("\n")

# 基本参数控制
scene.append_to_caption("初始角度(弧度): ")
slider_theta = slider(min=-pi, max=pi, value=0.5, length=200, bind=set_theta, right=15)
scene.append_to_caption("\n初始角速度(rad/s): ")
slider_omega = slider(min=-5, max=5, value=0, length=200, bind=set_omega, right=15)
scene.append_to_caption("\n小球质量(kg): ")
slider_mass = slider(min=0.05, max=0.5, value=0.1, length=200, bind=set_mass, right=15)
scene.append_to_caption("\n重力加速度(m/s²): ")
slider_gravity = slider(min=5, max=15, value=9.8, length=200, bind=set_gravity, right=15)
scene.append_to_caption("\n")

# 控制按钮
btn_run = button(text="开始", bind=toggle_run)
scene.append_to_caption("    ")
button(text="重置", bind=reset_all)
scene.append_to_caption("    ")
btn_record = button(text="开始记录", bind=toggle_recording)
scene.append_to_caption("    ")
button(text="导出数据", bind=export_data)
scene.append_to_caption("\n")

# 显示选项
button(text="切换矢量显示", bind=toggle_vectors)
scene.append_to_caption("    小球显示: ")
button(text="小球1", bind=lambda: toggle_ball_visibility(0))
scene.append_to_caption(" ")
button(text="小球2", bind=lambda: toggle_ball_visibility(1))
scene.append_to_caption(" ")
button(text="小球3", bind=lambda: toggle_ball_visibility(2))
scene.append_to_caption("\n\n")

# 实时数据显示
scene.append_to_caption("<b>实时数据</b>\n")
label_time = wtext(text="时间: 0.00 s")
scene.append_to_caption("\n")
label_speed = wtext(text="速度: 0.00 m/s")
scene.append_to_caption("\n")
label_ke = wtext(text="动能: 0.00 J")
scene.append_to_caption("\n")
label_pe = wtext(text="势能: 0.00 J")
scene.append_to_caption("\n")
label_te = wtext(text="总能量: 0.00 J")
scene.append_to_caption("\n")
label_acc = wtext(text="向心加速度: 0.00 m/s²")
scene.append_to_caption("\n\n")

# 图例
scene.append_to_caption("<b>图例</b>\n")
scene.append_to_caption("🔴 小球1 (质量: 0.10 kg)\n")
scene.append_to_caption("🔵 小球2 (质量: 0.15 kg)\n") 
scene.append_to_caption("🟢 小球3 (质量: 0.20 kg)\n")
scene.append_to_caption("🔵 速度矢量\n")
scene.append_to_caption("🟢 向心力矢量\n")
scene.append_to_caption("🟠 重力矢量\n")

# 主循环
dt = 0.002
sim_time = 0

while True:
    rate(500)
    
    if is_running:
        sim_time = time.time() - start_time
        
        # 更新所有小球
        for ball in balls:
            if ball.ball.visible:
                ball.update(dt)
        
        # 更新实时数据显示（当前选中的小球）
        current_ball = balls[current_ball_index]
        label_time.text = f"时间: {sim_time:.2f} s"
        label_speed.text = f"速度: {current_ball.speed:.2f} m/s"
        label_ke.text = f"动能: {current_ball.kinetic_energy:.3f} J"
        label_pe.text = f"势能: {current_ball.potential_energy:.3f} J"
        label_te.text = f"总能量: {current_ball.total_energy:.3f} J"
        label_acc.text = f"向心加速度: {current_ball.centripetal_acc:.2f} m/s²"
        
        # 更新能量图表
        if show_energy_graph and sim_time > 0:
            ke_curve.plot(sim_time, current_ball.kinetic_energy)
            pe_curve.plot(sim_time, current_ball.potential_energy)
            te_curve.plot(sim_time, current_ball.total_energy)
        
        # 记录数据
        if recording:
            for i, ball in enumerate(balls):
                if ball.ball.visible:
                    data_records.append([
                        round(sim_time, 3), ball.name, round(ball.theta, 4), 
                        round(ball.omega, 4), round(ball.speed, 4),
                        round(ball.kinetic_energy, 6), round(ball.potential_energy, 6),
                        round(ball.total_energy, 6), round(ball.centripetal_acc, 4)
                    ]) 
