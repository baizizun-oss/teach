# RecordService.py
import os
from pathlib import Path
import tornado.web
import myportal.common as common

import re
import logging


logger = logging.getLogger(__name__)

class RecordService(tornado.web.RequestHandler):
    def get(self):
        records = common.select("sangao", "SELECT * FROM record")
        self.render(
            os.path.join(common.BASE_DIR, "sangao", "templates", "Record", "lists.html"),
            records=records
        )




    def extract_teaching_chain(text: str):
        """
        从教学讲稿中提取递进式逻辑主线链条。
        返回一个字符串列表，每个元素是一个逻辑节点。
        """
        # 清理文本
        text = re.sub(r'\s+', ' ', text).strip()

        # 分句（保留中文标点）
        sentences = re.split(r'(?<=[。？！；])', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # 定义信号模式
        problem_patterns = [
            r'为什么.*[？?]',
            r'有什么.*缺点',
            r'是不是.*麻烦',
            r'还能不能',
            r'接下来.*需求',
            r'究竟什么是',
            r'最后.*需求',
            r'那怎么办',
            r'那是不是.*坏了'
        ]
        
        solution_patterns = [
            r'这就是(.+?)[。！]',
            r'所以(.+?)[。！]',
            r'对，(.+?)[。！]',
            r'于是(.+?)[。！]',
            r'这就是(.+?)的.*机制',
            r'(.+?)存在价值',
            r'(.+?)就是.+?地址'
        ]

        # 存储逻辑链
        chain = []
        current_problem = None

        i = 0
        while i < len(sentences):
            sent = sentences[i]

            # 检查是否是问题句
            is_problem = any(re.search(p, sent) for p in problem_patterns)
            # 检查是否是解决方案句
            sol_match = None
            for p in solution_patterns:
                m = re.search(p, sent)
                if m:
                    sol_match = m.group(1).strip()
                    break

            if is_problem:
                # 提取问题核心（简化）
                if "为什么" in sent:
                    if "IP" in sent:
                        current_problem = "需要网络地址"
                    elif "DNS" in sent or "麻烦" in sent:
                        current_problem = "手动查IP太麻烦"
                    elif "更快" in sent or "网速" in sent:
                        current_problem = "想让网络更快"
                    elif "搬家" in sent or "复用" in sent:
                        current_problem = "设备无法跨地复用"
                    else:
                        current_problem = "存在安全隐患或效率问题"
                elif "缺点" in sent:
                    current_problem = "无地址网络不安全"
                elif "需求" in sent:
                    if "更快" in sent:
                        current_problem = "追求更高网速"
                    else:
                        current_problem = "需要更普适的网络使用方式"
            elif sol_match:
                # 构造节点：如果前面有问题，则组合；否则单独作为知识点
                if current_problem:
                    node = f"{current_problem} → {sol_match}"
                    chain.append(node)
                    current_problem = None
                else:
                    chain.append(sol_match)
            elif "IPV四" in sent or "四个巴比特" in sent:
                chain.append("IP地址由4个0-255的数构成")
            elif "DNS" in sent and "服务器" in sent:
                chain.append("DNS自动将域名转为IP地址")
            elif "网速" in sent and "比特" in sent:
                chain.append("网速用每秒传输的比特数衡量")
            elif "带宽" in sent and ("水管" in sent or "最大速度" in sent):
                chain.append("带宽是网络的最大传输速率")
            elif "路由器" in sent and ("配置" in sent or "复用" in sent):
                chain.append("通过软件配置实现路由器多地复用")

            i += 1

        # 后处理：合并成连贯主线
        if not chain:
            return ["未能提取有效教学逻辑链"]

        # 尝试构建高层主线（基于你的期望格式）
        high_level_chain = []

        # 手动映射关键词到高层概念（可配置）
        mapping = {
            "安全隐患": "网络如何安全运行",
            "无地址网络不安全": "需要有地址的网络",
            "IP地址": "IP地址作为网络身份证",
            "手动查IP太麻烦": "传播过程太繁琐",
            "DNS": "引入DNS实现自动解析",
            "网速": "追求更快的传输速度",
            "带宽": "理解带宽限制",
            "路由器复用": "实现设备普适性"
        }

        # 构建高层链条
        seen = set()
        for item in chain:
            if "安全" in item or "无地址" in item:
                key = "网络如何安全运行"
            elif "IP" in item and "地址" in item:
                key = "有地址的网络，也就是IP地址"
            elif "麻烦" in item or "查IP" in item:
                key = "能运行了但太麻烦"
            elif "DNS" in item:
                key = "DNS自动解析"
            elif "更快" in item or "网速" in item:
                key = "方便了之后还想让他更快"
            elif "带宽" in item:
                key = "理解带宽限制"
            elif "路由器" in item and ("复用" in item or "配置" in item):
                key = "最后还想让他更普适"
            else:
                continue

            if key not in seen:
                high_level_chain.append(key)
                seen.add(key)

        # 如果高层链太短，回退到原始链
        if len(high_level_chain) < 2:
            return chain

        return high_level_chain