from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp 
import os 

@register("astrbot_plugin_zm", "yuki", "造梦小助手", "v1.1")
class MyPlugin(Star):
    IMAGE_MAP = {
    "宠物装备升级": "宠物装备升级.png",
    "宠物装备属性": "宠物装备属性.png",
    "灯谜": "灯谜.jpg",
    "法宝进阶": "法宝进阶.jpg",
    "技能耗蓝": "技能耗蓝.png",
    "剑阵": "剑阵.jpg",
    "煞戒合成": "煞戒合成.jpg",
    "生存大冒险": "生存大冒险.jpg",
    "头衔大全": "头衔大全.jpg",
    "装备强化": "装备强化.jpg",
    "坐骑装备": "坐骑装备.jpg",
    "BOSS掉落": "BOSS掉落.jpg",
    "BOSS属性": "BOSS属性.png",
    }

    def __init__(self, context: Context):
        super().__init__(context)
        self.plugin_dir = os.path.dirname(__file__) 

        self._lookup = {k.lower(): k for k in self.IMAGE_MAP.keys()}

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("zm") 
    async def strategy(self, event: AstrMessageEvent, opt: str = "菜单"): 
        '''返回对应类型的攻略图'''
        opt = opt.strip() # 消去多余空格

        # 发送菜单
        if opt in ("菜单", "帮助", "menu", "help"): 
            chain = [
                Comp.At(qq = event.get_sender_id()), 
                Comp.Plain(self._build_menu()) 
            ]
            yield event.chain_result(chain) 
            return 
        
        # 发送攻略图片
        # 查找时不区别大小写
        real_key = self._lookup.get(opt.lower()) 
        if real_key is not None: 
            # plugin_dir = os.path.dirname(__file__) 
            img_path = os.path.join(self.plugin_dir, "images", self.IMAGE_MAP[real_key]) 

            if not os.path.exists(img_path): 
                logger.error(f"图片不存在: {img_path}") 

                yield event.chain_result([
                    Comp.At(qq = event.get_sender_id()), 
                    Comp.Plain("图片没了😭， 可以 @清久必浊丶 补上") 
                ])
                return 
            
            yield event.chain_result([
                Comp.At(qq = event.get_sender_id()), 
                Comp.Image.fromFileSystem(img_path) 
            ])
            return 
        
        # 处理不存在的指令
        yield event.chain_result([
            Comp.At(qq = event.get_sender_id()),
            Comp.Plain("该指令不存在， 请发送 \"/zm 菜单\"查看全部指令")
        ])


    def _build_menu(self) -> str: 
        lines = ["📑提供如下攻略: "]
        for name in self.IMAGE_MAP.keys(): 
            lines.append(f"/zm {name}") 
        lines.append("如果您有更好的攻略图，可以私聊发送给我！")
        lines.append("如果您是图片的作者且不想要我使用您的图片，请联系我，我会及时删除的！")
        return '\n'.join(lines) 


    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
