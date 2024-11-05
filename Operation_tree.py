import keyboard
from collections import deque
from graphviz import Digraph

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = {}
        self.parent = None
        self.is_end_of_sequence = False

class MultiTree:
    def __init__(self):
        self.root = TreeNode('root')

    def add_sequence(self, sequence):
        current = self.root
        for key in sequence.split('+'):
            temp_key_node = TreeNode(key)
            if key not in current.children:
                current.children[key] = temp_key_node
                temp_key_node.parent = current
            current = current.children[key]
        current.is_end_of_sequence = True


    
    def visualize_tree(self, node=None, graph=None):
        """ 可视化树结构 """
        if graph is None:
            graph = Digraph('MultiTree')
        if node is None:
            node = self.root
        # 打印当前节点
        graph.node(node.value)
        # 遍历子节点
        for child in node.children.values():
            graph.node(child.value)
            graph.edge(node.value, child.value)  # 连接父节点和子节点
            self.visualize_tree(child, graph)  # 递归处理子节点

        return graph

# 创建多叉树并添加操作序列
tree = MultiTree()
tree.add_sequence("ctrl+up+4")
tree.add_sequence("ctrl+down+v")
tree.add_sequence("ctrl+down+g")
tree.add_sequence("f")
# 可视化树的结构
dot_graph = tree.visualize_tree()
dot_graph.render('multi_tree', format='png', cleanup=True)  # 生成图片并保存

# # 使用队列存储按键
input_queue = deque()
current_node = tree.root  # 从根节点开始

# # 按键回调函数
def on_key_event(event):
    global input_queue
    global current_node
    if event.name in current_node.children:  # 如果当前输入在子节点中
        input_queue.append(event.name)  # 将按键压入队列
        print(f"当前输入序列:{input_queue}")
        current_node = current_node.children[event.name]  # 切换到子节点
        print(f"当前节点:{current_node.value}")
        if current_node.is_end_of_sequence:  # 如果到达终点
            print('匹配成功')
            input_queue.clear()  # 清空队列
            current_node = tree.root  # 回到根节点
        else:
            return
    else:
        if current_node.value == 'root':  # 如果当前节点是根节点
            return
        if current_node.parent.value in ['root',None]:  # 如果当前节点不是根节点
            return
        if current_node.parent.value == event.name:  # 如果当前输入是父节点的按键
                current_node = current_node.parent  # 回退到父节点
                input_queue.pop()  # 弹出最后一个按键
                print(f"当前输入序列:{input_queue}")
                return 
        if event.name in current_node.parent.children:  # 如果当前输入是父节点的子节点的按键
            return


# 注册热键监听
keyboard.on_press(on_key_event)

#4. 维持程序4运行，直到用户手动停止
print("按 'esc' 键退4出程序...")
keyboard.wait('esc')
