import keyboard
from collections import deque
from graphviz import Digraph

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = {}
        self.is_end_of_sequence = False

class MultiTree:
    def __init__(self):
        self.root = TreeNode('')

    def add_sequence(self, sequence):
        current = self.root
        for key in sequence.split('+'):
            if key not in current.children:
                current.children[key] = TreeNode(key)
            current = current.children[key]
        current.is_end_of_sequence = True

    def match_sequence(self, keys):
        current = self.root
        for key in keys:
            if key in current.children:
                current = current.children[key]
                if current.is_end_of_sequence:
                    return True
            else:
                break
        return False

    def get_valid_sequence(self, current_sequence):
        """ 获取当前序列的有效部分 """
        valid_sequence = []
        current = self.root
        for key in current_sequence:
            if key in current.children:
                valid_sequence.append(key)
                current = current.children[key]
            else:
                break
        return valid_sequence
    
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
tree.add_sequence("right ctrl+up+4")
tree.add_sequence("right ctrl+down+v")
tree.add_sequence("right ctrl+down+g")
tree.add_sequence("right ctrl+left+ctrl")
# 可视化树的结构
dot_graph = tree.visualize_tree()
dot_graph.render('multi_tree', format='png', cleanup=True)  # 生成图片并保存

# 使用队列存储按键
input_queue = deque()

# 按键回调函数
def on_key_event(event):
    global input_queue
    if event.name == "ctrl":
        # 如果按下了ctrl，则重置队列，并加入ctrl
        input_queue.clear()
        input_queue.append(event.name)
    else:
        # 按下其他键时，先加入键，然后检查是否有效
        input_queue.append(event.name)

        # 获取当前有效的按键序列
        valid_sequence = tree.get_valid_sequence(list(input_queue))

        # 更新队列为有效序列
        input_queue.clear()
        input_queue.extend(valid_sequence)

    # 检查是否能够匹配到完整的操作序列
    if tree.match_sequence(list(input_queue)):
        print(f"匹配成功: {'+'.join(input_queue)}")
        input_queue.clear()
    else:
        print(f"当前匹配: {'+'.join(input_queue)}")

# 注册热键监听
keyboard.on_press(on_key_event)

#4. 维持程序运行，直到用户手动停止
print("按 'esc' 键退出程序...")
keyboard.wait('esc')
# def generate_intervals(total, intervals):
#     start = 1  # 起始值
#     result = []

#     for interval in intervals:
#         end = start + interval - 1  # 计算结束值
        
#         if end > total:  # 如果结束值超过总数，则调整为总数
#             end = total
            
#         result.append((start, end))  # 保存当前的起始和结束
#         start = end + 1  # 更新下一个起始值

#         if start > total:  # 如果起始值超出总数，提前终止循环
#             break

#     return result

# # 示例
# total = 21
# intervals = [2, 3, 6, 9]
# output = generate_intervals(total, intervals)
# print(output)v
