class Trade_Info:

    def __init__(self, goods):
        # 礼物 或 心愿 总数
        self.total = 0
        # viewmodel的实际数据
        self.trade = []
        self.__parse(goods)

    # 处理一组的数据
    def __parse(self, goods):
        self.total = len(goods)
        self.trade = [self.__map_to_trade(single) for single in goods]

    # 处理单独数据 把原始数据处理成网页需要的数据
    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )
