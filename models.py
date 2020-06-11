from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    """ 资产总表 """
    device_type_choices = (
            ('server', u'服务器'),
            ('switch', u'交换机'),
            ('router', u'路由器'),
            ('ddos', u'高防'),
            ('database', u'数据库'),
            ('slb', u'负载均衡'),
            ('others', u'其它类'),
    )
    asset_status = (
        (0, '运行中'),
        (1, '已停止'),
        (2, '已过期'),
        (3, '即将过期'),
        (4, '启动中'),
        (5, '停止中'),
        (6, '已锁定'),
        (7, '等待释放'),
    )

    pay_type_choices = (
        (0, '包年包月'),
        (1, '按量付费'),
    )

    renewal_type_choices = (
        (0, '手动续费'),
        (1, '自动续费'),
    )

    virtual_machine_choices = (('physical', '物理机'),
                               ('tencent', 'tencent'),
                               ('aliyun', 'aliyun'),
    )

    # environment_choices = (('testing', u'测试环境'), ('production', u'生产环境'))

    func_choices = [(item, item) for item in settings.FUNC_LIST]

    device_type = models.CharField('设备类型', choices=device_type_choices, max_length=64, default='server')
    name = models.CharField('资产名称', max_length=30, blank=True, null=True, unique=True)
    sn = models.CharField('资产序列号', max_length=128, unique=True)  # 等同于实例ID
    status = models.SmallIntegerField('设备状态', choices=asset_status, default=0)
    tag = models.ManyToManyField('Tag', null=True, blank=True)
    virtual_machine = models.CharField(choices=virtual_machine_choices, max_length=64, default='physical')

    # environment = models.CharField(choices=environment_choices, max_length=64, default='production')
    hostname = models.CharField(max_length=128, blank=True, unique=True)
    asset_op = models.CharField(max_length=64, blank=True, null=True)
    contract = models.ForeignKey('Contract', verbose_name=u'合同', null=True, blank=True, on_delete=models.SET_NULL)
    trade_time = models.DateField(u'创建时间', null=True, blank=True)
    expire_time = models.DateField(u'过期时间', null=True, blank=True)
    renewal_way = models.SmallIntegerField('续费方式', choices=renewal_type_choices, max_length=64, blank=True, null=True)
    pay_way = models.SmallIntegerField('付费方式', choices=pay_type_choices, max_length=64, blank=True, null=True)
    # warranty = models.SmallIntegerField(u'保修期', null=True, blank=True)
    price = models.FloatField(u'价格', null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'属于的业务线', null=True, blank=True)

    function = models.CharField('套餐类型', choices=func_choices, max_length=64, default='WEB', blank=True, null=True)
    purpose = models.CharField('套餐详情', max_length=200, blank=True, null=True)
    admin = models.ForeignKey('UserProfile', verbose_name=u'设备管理员', related_name='+', null=True, blank=True,
                              on_delete=models.PROTECT)
    proposer = models.ForeignKey('UserProfile', verbose_name=u'申请人', related_name='user_proposer', null=True,
                                 blank=True, on_delete=models.PROTECT)
    idc = models.ForeignKey('IDC', verbose_name=u'IDC机房', null=True, blank=True, on_delete=models.SET_NULL)
    idc_room = models.ForeignKey('idcapp.IDCRoom', verbose_name=u'物理机房', null=True, blank=True,
                                 on_delete=models.SET_NULL)

    thick = models.CharField(u'资产U数', max_length=100, null=True, blank=True)
    description = models.TextField(u'备注', null=True, blank=True)

    import_user = models.ForeignKey(User, verbose_name=u"导入人", null=True, blank=True, on_delete=models.PROTECT)
    create_at = models.DateTimeField('创建日期', blank=True, auto_now_add=True)
    update_at = models.DateTimeField('更新日期', blank=True, auto_now=True)
    setup_at = models.DateTimeField(blank=True, null=True)
    apply_at = models.DateTimeField(blank=True, null=True)

    ratio = models.CharField(u'资产利用率', max_length=16, blank=True, null=True)

    class Meta:
        db_table = 'cmdb_asset'
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"

    def __str__(self):
        return 'id:%s h:%s' % (self.id, self.hostname)


class Server(models.Model):
    """服务器表"""

    sub_asset_type_choice = (
        (0, 'ecs'),
        (1, 'rds'),
        (2, 'mongo'),
        (3, 'redis'),
    )

    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！asset被删除的时候一并删除server
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="服务器类型")
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name="添加方式")
    server_type = models.IntegerField("服务器类型", choices=type_choices, default=0)
    server_ID = models.CharField('服务器ID', max_length=100)
    image_ID = models.CharField('镜像ID', max_length=100)
    server_area = models.CharField('服务器所在区', max_length=100)
    server_name = models.CharField('服务器名称', max_length=50)

    cpu = models.IntegerField('实例cpu')
    memory = models.IntegerField('实例内存')
    capacity = models.IntegerField('实例硬盘容量', null=True)
    description = models.TextField("描述", blank=True)

    instance_type = models.CharField('实例类型', max_length=100, blank=True, null=True)
    os = models.CharField('操作系统', max_length=100, blank=True)
    Flexible_net = models.CharField('弹性网卡', max_length=100, null=True)
    public_ip = models.CharField('公网IP', max_length=100)
    Flexible_net_ip = models.CharField('弹性公网IP', max_length=100, null=True)
    private_ip = models.CharField('私有IP', max_length=100)
    port = models.IntegerField("服务端口", null=True)
    user_name = models.CharField('用户名', max_length=32, null=True)
    password = models.CharField('密码', max_length=32, null=True)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        db_table = 'cmdb_server'
        verbose_name = '服务器'
        verbose_name_plural = "服务器"


class Switch(models.Model):
    """交换机"""
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！asset被删除的时候一并删除server
    pass


class Slb(models.Model):
    """负载均衡表"""
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！asset被删除的时候一并删除server
    pass


class Router(models.Model):
    """路由器表"""
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！asset被删除的时候一并删除server
    pass


class Ddos(models.Model):
    """高防表"""
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！asset被删除的时候一并删除server
    pass


class IDC(models.Model):
    """ 机房表 """
    name = models.CharField(u'机房名称', max_length=50, unique=True)
    description = models.TextField(u'机房说明', null=True, blank=True)


class Tag(models.Model):
    """标签"""
    name = models.CharField('Tag name', max_length=32, null=True, blank=True, unique=True)
    creater = models.ForeignKey('User', verbose_name='创建者', blank=True, null=True, on_delete=models.PROTECT)
    description = models.CharField('Tag描述', max_length=64, null=True, blank=True)
    create_time = models.DateTimeField('创建日期', blank=True, null=True, auto_now_add=True)
    update_time = models.DateTimeField('更新日期', blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb_tag'
        verbose_name = '标签表'
        verbose_name_plural = "标签表"


class BusinessUnit(models.Model):
    """业务线表"""
    name = models.CharField('业务线名称', max_length=64)
    owners = models.CharField('业务线负责人', max_length=64, null=True)
    ops_contact = models.ManyToManyField('UserProfile', verbose_name=u'运维专员', related_name='ops', default=None,
                                         null=True, blank=True)
    # op_user = models.ForeignKey('OpUser', related_name='opuser', verbose_name=u"业务线对应运维", null=True, blank=True)
    # domain = models.ForeignKey('Domain', verbose_name=u"业务线所属域名", null=True, blank=True)
    description = models.TextField("描述", blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 'cmdb_business_unit'
        verbose_name = "业务线表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProductUnit(models.Model):
    """产品线表"""
    name = models.CharField('产品线名称', max_length=64)
    description = models.TextField("描述", blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'属于的业务线', null=True, blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 'cmdb_product_unit'
        verbose_name = "产品线表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# class OpUser(models.Model):
#     """运维人员表"""
#     name = models.CharField('运维人员名称', max_length=64)
#     email = models.CharField('邮箱', max_length=128)
#     phone = models.CharField('联系电话', max_length=128)
#     description = models.TextField("描述", blank=True)
#     create_time = models.DateTimeField("创建时间", auto_now_add=True)
#     update_time = models.DateTimeField("更新时间", auto_now=True)
#
#     class Meta:
#         db_table = 'cmdb_business_unit'
#         verbose_name = "运维表"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name


class Domain(models.Model):
    """域名表"""
    name = models.CharField('域名名称', max_length=64)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'属于的业务线', null=True, blank=True)
    description = models.TextField("描述", blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 'cmdb_business_unit'
        verbose_name = "域名表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#### BEGIN **用户管理 相关 model #######################################
class UserProfile(models.Model):
    """用户资料表"""
    types_choice = {
        ('department-manager', u'部门经理'),
        ('employee', u'普通员工')
    }

    user = models.OneToOneField(User)
    name = models.CharField(u'名字', max_length=32)
    token = models.CharField(u'token', max_length=128, blank=True, null=True)
    types = models.CharField(choices=types_choice, verbose_name=u'用户类型', max_length=30, default='employee')
    business_unit = models.ForeignKey(BusinessUnit, verbose_name=u'业务线')
    email = models.EmailField(u'邮箱')
    mobile = models.CharField(u'手机', max_length=32)
    employee_id = models.CharField(u'员工编号', max_length=32, default=None, blank=True, null=True)

    leader = models.ForeignKey('self', verbose_name=u'上级领导', blank=True, null=True, on_delete=models.PROTECT)
    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField("创建时间", blank=True, auto_now_add=True)
    update_at = models.DateTimeField("更新时间", blank=True, auto_now=True)
    # roles = models.ManyToManyField(u'Roles', verbose_name=u'用户角色', blank=True, null=True)
    permissions = models.ManyToManyField(u'Menus', through='UserMenus', verbose_name=u'用户菜单权限', blank=True, null=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = "用户信息"

    def __str__(self):
        if self.employee_id:
            return u"{name}({employee_id})".format(name=self.name, employee_id=self.employee_id)
        else:
            return u"{name}".format(name=self.name)


class Menus(LogOnUpdateDeleteModel):
    name = models.CharField(u'菜单名称', max_length=100, null=False, blank=False)
    parent = models.ForeignKey('self', verbose_name=u'父菜单', blank=True, null=True, on_delete=models.PROTECT)
    url = models.CharField(u'菜单URL', max_length=100, null=True, blank=True)
    get = models.CharField(u'查看权限', max_length=10, default='0')
    post = models.CharField(u'修改权限', max_length=10, default='0')
    put = models.CharField(u'新增权限', max_length=10, default='0')
    delete = models.CharField(u'删除权限', max_length=10, default='0')
    sort = models.IntegerField(u'排序', blank=True, null=True)
    is_active = models.BooleanField(u'是否激活', default=False)
    description = models.TextField(u'描述', max_length=500, null=False, blank=False)
    create_at = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    update_at = models.DateTimeField(blank=True, auto_now=True, null=True)

    def __unicode__(self):
        return '%s:%s' % (self.id, self.name)

    class Meta:
        ordering = ('sort', 'id',)
        verbose_name = '权限菜单表'
        verbose_name_plural = "权限菜单表"


class UserMenus(models.Model):
    """用户权限表"""
    userprofile = models.ForeignKey(u'UserProfile', on_delete=models.PROTECT)
    menu = models.ForeignKey(u'Menus', on_delete=models.PROTECT)
    get = models.CharField(u'查看权限', max_length=10, default='0')
    post = models.CharField(u'修改权限', max_length=10, default='0')
    put = models.CharField(u'新增权限', max_length=10, default='0')
    delete = models.CharField(u'删除权限', max_length=10, default='0')
    description = models.TextField(u'描述', max_length=500, null=False, blank=False)
    create_at = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    update_at = models.DateTimeField(blank=True, auto_now=True, null=True)

    def __unicode__(self):
        return '%s,%s' % (self.id, self.userprofile)

    class Meta:
        db_table = 'cmdb_userprofile_menus'
        verbose_name = '用户权限表'
        verbose_name_plural = "用户权限表"
