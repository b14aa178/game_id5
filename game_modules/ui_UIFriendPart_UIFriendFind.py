# uncompyle6 version 3.1.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.3 (default, Apr 28 2018, 18:36:20) 
# [GCC 7.3.1 20180312]
# Embedded file name: ui\UIFriendPart\UIFriendFind.py
Instruction context:
   
 418      13  POP_JUMP_IF_FALSE    17  'to 17'
             16  LOAD_GLOBAL           0  'True'
             19  RETURN_VALUE     
             20  LOAD_GLOBAL           1  'False'
->           23  RETURN_VALUE     
from cocosui import cc, ccui
import re, time, game_kernel as GK
from common_tools import utils
from common_cs import ComuKeys
from consts import const
import debug_log
from UIFriendBase import UIFriendBase
from ui.ListViewAdapter import ListViewItemBase, RankListViewAdapter
from ui.CommonTextFieldHandler import CommonTextFieldHandler

class ApplyItem(ListViewItemBase):

    def __init__(self, widget, master=None):
        super(ApplyItem, self).__init__(widget, master)
        self.master = master

    def ui_mail_has_read(self):
        self.hint.setVisible(False)
        self.text_name.setTextColor(cc.Color4B(67, 66, 65, 255))
        self.text_time.setTextColor(cc.Color4B(67, 66, 65, 255))
        self.ico_read.setVisible(True)
        utils.set_gray(self.ico_type)

    def update_data(self, t_info):
        func = ccui.Helper.seekNodeByName
        btn_player = func(self.widget, 'btn_player')
        btn_player.addTouchEventListener(utils.call_on_touch_ended_custom(self.master.on_item_friend_find1, t_info))
        self.master.bind_button(btn_player, 'btn_no', cb=self.master.on_btn_apply_friend_no, cb_params=t_info['uid'])
        self.master.bind_button(btn_player, 'btn_yes', cb=self.master.on_btn_apply_friend_yes, cb_params=t_info['uid'])
        name_widget = func(btn_player, 'text_name')
        func(btn_player, 'text_name').setString(t_info['name'])
        func(btn_player, 'text_verify').setString(t_info['message'])
        p_face = func(btn_player, 'p_face')
        self.p_s = func(btn_player, 'p_s')
        self.p_h = func(btn_player, 'p_h')
        func(self.p_h, 'text_lv_h').setString(str(t_info['b_lv']))
        func(self.p_s, 'text_lv_s').setString(str(t_info['c_lv']))
        face_frame_id = t_info.get('face_frame_id', GK.DM.default_face_frame_id)
        self.master.load_face_img(t_info['face_id'], face_frame_id, p_face, t_info.get('online_stat', 1))
        func(p_face, 'bg_face').addTouchEventListener(utils.call_on_touch_ended_custom(self.master.on_item_friend_find1, t_info))
        gender = t_info.get('gender')
        ico_sex = func(btn_player, 'ico_sex')
        if gender in (0, 1):
            path = 'common/ico_sex_%s.png' % ('male' if gender == 1 else 'female')
            utils.load_texture(ico_sex, path)
        else:
            ico_sex.setVisible(False)
        civilian_part = t_info.get('c_part', 1)
        civilian_part_lv = t_info.get('c_part_lv', 1)
        unit_type = ComuKeys.UNIT_TYPE_CONF.CIVILIAN
        ico_rank_s = func(self.p_s, 'ico_rank_s')
        GK.g_ui_mgr.set_icon_png(ico_rank_s, civilian_part, civilian_part_lv, unit_type, format='small')
        butcher_part = t_info.get('b_part', 1)
        butcher_part_lv = t_info.get('b_part_lv', 1)
        unit_type = ComuKeys.UNIT_TYPE_CONF.BUTCHER
        ico_rank_h = func(self.p_h, 'ico_rank_h')
        GK.g_ui_mgr.set_icon_png(ico_rank_h, butcher_part, butcher_part_lv, unit_type, format='small')
        utils.range_player_info_node(gender, name_widget, ico_sex, self.p_s, self.p_h)

    def destroy(self):
        super(ApplyItem, self).destroy()
        self.master = None
        return


class UIFriendFind(UIFriendBase):
    CSB_PATH = 'ui/dm65ui/res/friend_find.csb'
    MAX_LEN = 9

    def __init__(self, parent_widget, y_position):
        super(UIFriendFind, self).__init__(parent_widget)
        func = ccui.Helper.seekNodeByName
        p_find = func(self.root_node, 'p_find')
        self.switch_tab = func(p_find, 'switch_tab')
        self.touch_recommend = func(self.switch_tab, 'touch_recommend')
        self.touch_recommend.addTouchEventListener(utils.call_on_touch_ended_custom(self.on_switch_list, None))
        self.touch_application = func(self.switch_tab, 'touch_application')
        self.touch_application.addTouchEventListener(utils.call_on_touch_ended_custom(self.on_switch_list, None))
        self.list_recommend = func(p_find, 'list_recommend')
        self.item_recommend = func(p_find, 'item_recommend')
        self.item_recommend.setVisible(False)
        self.list_application = func(p_find, 'list_application')
        self.item_application = func(p_find, 'item_application')
        self.item_application.setVisible(False)
        self.apply_list_adapter = RankListViewAdapter(self.list_application)
        self.apply_list_adapter.BATCH_NUM = 8
        self.apply_list_adapter.LIST_VIEW_ITEM_UPPER = 16
        self.apply_list_adapter.set_create_item_func(self.create_apply_item)
        self.text_name = p_find.getChildByName('text_name')
        self.text_name.setString(GK.g_avatar.player_name)
        self.text_id = p_find.getChildByName('text_id')
        self.text_id.setString('ID: ' + GK.g_avatar.unique_id)
        self.img_qr_code = func(p_find, 'img_qr_code')
        self.init_qr_code()
        self.btn_refresh = p_find.getChildByName('btn_refresh')
        self.btn_delete_all = p_find.getChildByName('btn_delete_all')
        self.btn_qr_code = p_find.getChildByName('btn_qr_code')
        self.btn_qr_code.setVisible(False)
        self.bind_button(p_find, 'btn_search', cb=self.on_btn_search)
        self.bind_button(p_find, 'btn_del', cb=self.on_btn_del)
        self.bind_button(p_find, 'btn_refresh', cb=self.on_btn_refresh)
        self.bind_button(p_find, 'btn_delete_all', cb=self.on_btn_delete_all)
        self.bind_button(p_find, 'btn_qr_code', cb=self.on_btn_sacn_code)
        self.bind_button(p_find, 'btn_input_code', cb=self.on_btn_input_code)
        self.last_search_time = 0
        input_find = func(p_find, 'input_find')
        self.input_message_handler = CommonTextFieldHandler(input_find)
        self.input_message_handler.set_max_length_enabled(True)
        self.input_message_handler.set_max_length(self.MAX_LEN)
        self.input_message_handler.set_placeholder(utils.do_ui_tid_replace('TXT_FRIEND_SEARCH_HINT'))
        self.uid_to_btn_player = {}
        self.button_share_link = func(p_find, 'btn_send_url')
        from etc import pack_config
        self.button_share_link.setVisible(GK.g_sdk_mgr.is_share_link_enabled() and pack_config.is_chs_type())
        self.bind_button(p_find, 'btn_send_url', cb=self.on_button_share)
        return

    def init_qr_code(self):
        from ui.UIArticleItem import UIArticleItem
        self.img_qr_code.setScale(0.01, 0.01)
        face_node = UIArticleItem().get_item_widget(ComuKeys.ARTICLE_TYPE.FACE, GK.g_avatar.face_id)
        p_cover = face_node.getChildByName('p_cover')
        GK.g_ui_mgr.set_face_frame_png(p_cover, GK.g_avatar.face_frame_id)
        face_node.setAnchorPoint(cc.Vec2(0.5, 0.5))
        face_node.setScale(120, 120)
        self.img_qr_code.addChild(face_node)
        return
        from core.SDKManager import SDKManager
        mgr = SDKManager.instance()
        qr_img = 'self.png'

        def cb(path):
            import game3d, shutil, os
            shutil.copyfile(path, os.path.join(game3d.get_doc_dir(), 'res', qr_img))
            self.img_qr_code.loadTexture(qr_img)

        uid = str(GK.g_avatar.unique_id)
        mgr.create_qr_code(uid, 100, 100, qr_img, cb)

    def create_apply_item(self, arg):
        item = ApplyItem(self.item_application.clone(), self)
        item.setVisible(True)
        return item

    def just_show(self):
        self.root_node.setVisible(True)

    def update_hint(self):
        hint_widget = self.touch_application.getChildByName('hint')
        hint_widget.setVisible(len(GK.g_avatar.rec_apply_list) > 0)

    def show(self):
        super(UIFriendFind, self).show()
        self.show_friend_apply_func()
        self.show_friend_find_func(None)
        self.on_switch_list(self.touch_recommend, None)
        self.update_hint()
        return

    def destroy(self):
        self.apply_list_adapter.destroy()
        self.apply_list_adapter = None
        super(UIFriendFind, self).destroy()
        return

    def hand_name_event(self):

        def handler(widget, event):
            if event == ccui.TEXTFIELD_EVENT_INSERT_TEXT:
                name = widget.getString()
                name = utils.strQ2B(name)
                widget.setString(name)

        return handler

    def on_switch_list(self, btn_widget, event):
        if btn_widget is self.touch_recommend:
            self.touch_recommend.getChildByName('img_slc').setVisible(True)
            hint_text_color = utils.color_code_2_rgb('3b2714', 255)
            self.touch_recommend.getChildByName('text').setTextColor(hint_text_color)
            self.touch_recommend.getChildByName('text').setFontSize(60)
            self.touch_application.getChildByName('img_slc').setVisible(False)
            none_text_color = utils.color_code_2_rgb('c6b692', 255)
            self.touch_application.getChildByName('text').setTextColor(none_text_color)
            self.touch_application.getChildByName('text').setFontSize(48)
            self.list_recommend.setVisible(True)
            self.list_application.setVisible(False)
            self.btn_refresh.setVisible(True)
            self.btn_delete_all.setVisible(False)
        if btn_widget is self.touch_application:
            self.touch_recommend.getChildByName('img_slc').setVisible(False)
            none_text_color = utils.color_code_2_rgb('c6b692', 255)
            self.touch_recommend.getChildByName('text').setTextColor(none_text_color)
            self.touch_recommend.getChildByName('text').setFontSize(48)
            self.touch_application.getChildByName('img_slc').setVisible(True)
            hint_text_color = utils.color_code_2_rgb('3b2714', 255)
            self.touch_application.getChildByName('text').setTextColor(hint_text_color)
            self.touch_application.getChildByName('text').setFontSize(60)
            self.list_recommend.setVisible(False)
            self.list_application.setVisible(True)
            self.btn_refresh.setVisible(False)
            self.btn_delete_all.setVisible(True)

    def on_btn_del(self, btn):
        self.input_message_handler.reset()

    def on_btn_refresh(self, btn):
        info = GK.g_avatar.refresh_friend_recommend()
        if info:
            self.show_friend_find_func(info)

    def on_button_share(self, button):
        GK.g_ui_mgr.UIShareEntrance.show(self._on_select_share)

    def _on_select_share(self, channel, cycle=True):
        has_app = GK.g_sdk_mgr.has_share_app_installed(channel, cycle)
        if not has_app:
            GK.g_ui_mgr.show_tips(utils.do_ui_tid_replace('TID_CANNOT_SHARE'))
            return
        share_log_info = {'content_type': 4}
        GK.g_sdk_mgr.share_links_to_friends(channel, cycle, share_log_info=share_log_info)

    def on_btn_delete_all(self, btn):
        GK.g_ui_mgr.show_confirm_dialog(utils.do_ui_tid_replace('TID_CONFIRM_DELETE_ALL_FRIEND_APPLICATION'), yes_cb=self.do_delete_all)

    def do_delete_all(self):
        GK.g_avatar.do_delete_all_friend_apply()
        self.show_friend_apply_func()

    def on_btn_search(self, btn):
        name = self.input_message_handler.get_whole_text()
        name = utils.strQ2B(name)
        name = name.strip()
        if not name:
            GK.g_ui_mgr.show_tips(utils.do_ui_tid_replace('TID_TEXT_SEARCH_NULL'))
            return
        new_name = ('').join(name.split(' '))
        if new_name != name:
            return
        result = re.findall(u'[^\u4e00-\u9fa5a-zA-Z0-9]', name.decode('utf-8'))
        if len(result) != 0:
            GK.g_ui_mgr.show_tips(utils.do_ui_tid_replace('TID_PROMPT_NOT_FIND_PLAYER'))
            return
        result2 = re.findall(u'[\u4e00-\u9fa5a-zA-Z0-9]', name.decode('utf-8'))
        if len(result2) > self.MAX_LEN:
            return
        GK.g_ui_mgr.show_ui('UILoadingHint', {'auto_hide': True})
        current_time = time.time()
        if current_time - GK.g_avatar.last_search_time < GK.DM.global_data['friend_search_delta']:
            GK.g_ui_mgr.show_tips(utils.do_ui_tid_replace('TID_TEXT_SEARCH_FREQUENTLY'))
            return
        GK.g_avatar.last_search_time = current_time
        if name.isdigit():
            GK.g_avatar.call_server_method('search_uid', {'uid': name})
        else:
            GK.g_avatar.call_server_method('search_name', {'name': name})

    def show_friend_find_func(self, info):
        if not info:
            info = []
        self.on_switch_list(self.touch_recommend, None)
        self.list_recommend.removeAllItems()
        self.uid_to_btn_player = {}
        func = ccui.Helper.seekNodeByName
        for t_info in info:
            t_item = self.item_recommend.clone()
            self.list_recommend.pushBackCustomItem(t_item)
            t_item.setVisible(True)
            btn_player = func(t_item, 'btn_player')
            self.uid_to_btn_player[t_info['_id']] = btn_player
            btn_player.addTouchEventListener(utils.call_on_touch_ended_custom(self.on_item_friend_find, t_info))
            btn_add = func(btn_player, 'btn_add')
            btn_add.setVisible(True)
            text_name = func(btn_player, 'text_name')
            text_name.setString(t_info['name'])
            self.p_s = func(btn_player, 'p_s')
            self.p_h = func(btn_player, 'p_h')
            gender = t_info.get('gender')
            ico_sex = func(t_item, 'ico_sex')
            if gender in (0, 1):
                path = 'common/ico_sex_%s.png' % ('male' if gender == 1 else 'female')
                utils.load_texture(ico_sex, path)
            else:
                ico_sex.setVisible(False)
            if t_info['online_stat']:
                text_name.setTextColor(utils.color_code_2_rgb('553c2d', 255))
            else:
                text_name.setTextColor(cc.Color4B(67, 66, 65, 255))
            name_widget = func(btn_player, 'text_name')
            func(btn_player, 'text_lv_h').setString(str(t_info['butcher_data']['lv']))
            func(btn_player, 'text_lv_s').setString(str(t_info['civilian_data']['lv']))
            p_face = func(btn_player, 'p_face')
            text_state = func(btn_player, 'text_state')
            text_state.setVisible(False)
            face_frame_id = t_info.get('face_frame_id', GK.DM.default_face_frame_id)
            self.load_face_img(t_info['face_id'], face_frame_id, p_face, t_info.get('online_stat', 1))
            self.bind_button(btn_player, 'btn_add', cb=self.on_btn_add_friend, cb_params=[t_info['_id'], btn_player])
            func(p_face, 'bg_face').addTouchEventListener(utils.call_on_touch_ended_custom(self.on_item_friend_find, t_info))
            civilian_part = t_info['civilian_data']['part']
            civilian_part_lv = t_info['civilian_data']['part_lv']
            unit_type = ComuKeys.UNIT_TYPE_CONF.CIVILIAN
            ico_rank_s = func(self.p_s, 'ico_rank_s')
            GK.g_ui_mgr.set_icon_png(ico_rank_s, civilian_part, civilian_part_lv, unit_type, format='small')
            butcher_part = t_info['butcher_data']['part']
            butcher_part_lv = t_info['butcher_data']['part_lv']
            unit_type = ComuKeys.UNIT_TYPE_CONF.BUTCHER
            ico_rank_h = func(self.p_h, 'ico_rank_h')
            GK.g_ui_mgr.set_icon_png(ico_rank_h, butcher_part, butcher_part_lv, unit_type, format='small')
            utils.range_player_info_node(gender, name_widget, ico_sex, self.p_s, self.p_h)

        return

    def load_face_img(self, face_id, face_frame_id, p_face, online_stat):
        func = ccui.Helper.seekNodeByName
        func(p_face, 'bg_face').setTouchEnabled(True)
        GK.g_ui_mgr.set_face_png(p_face, face_id, face_frame_id, online_stat)

    def on_item_friend_find(self, btn, t_info):
        unique_id = t_info['_id']
        self._on_item_friend_find(btn, t_info, unique_id)

    def on_item_friend_find1(self, btn, t_info):
        unique_id = t_info['uid']
        self._on_item_friend_find(btn, t_info, unique_id)

    def _on_item_friend_find(self, btn, t_info, unique_id):
        GK.g_avatar.show_player_item_tips(btn, t_info, unique_id)

    def on_btn_add_friend(self, btn, uid_btn_player):
        uid = uid_btn_player[0]
        btn_player = uid_btn_player[1]
        GK.g_ui_mgr.show_ui('UIFriendVerify', args={'uid': uid})

    def on_btn_sacn_code(self, btn):

        def cb(code, content):
            GK.g_avatar.call_server_method('search_qr_code', {'uid': content})

        from core.SDKManager import SDKManager
        mgr = SDKManager.instance()
        mgr.scan_qr_code(cb)

    def on_btn_input_code(self, btn):
        GK.g_ui_mgr.show_ui('UIFriendFaceToFace')

    def ask_add_friend_cb(self, uid):
        btn_player = self.uid_to_btn_player.get(uid)
        if not btn_player:
            return
        func = ccui.Helper.seekNodeByName
        try:
            btn_add = func(btn_player, 'btn_add')
            btn_add.setVisible(False)
            text_state = func(btn_player, 'text_state')
            text_state.setVisible(True)
        except Exception as e:
            pass

    def show_friend_apply_func(self):
        self.apply_list_adapter.update_data(GK.g_avatar.get_rec_apply_list())

    def on_btn_apply_friend_no(self, btn, uid):
        self.on_btn_apply_friend_index(uid)
        GK.g_avatar.reject_be_friend(uid)

    def on_btn_apply_friend_yes(self, btn, uid):
        if GK.g_avatar.do_agree_be_friend(uid):
            self.on_btn_apply_friend_index(uid)

    def on_btn_apply_friend_index(self, uid):

        def the_filter--- This code section failed: ---

 417       0  LOAD_FAST             0  'val'
           3  LOAD_CONST            1  'uid'
           6  BINARY_SUBSCR    
           7  LOAD_DEREF            0  'uid'
          10  COMPARE_OP            2  '=='

 418      13  POP_JUMP_IF_FALSE    17  'to 17'
          16  LOAD_GLOBAL           0  'True'
          19  RETURN_VALUE     
          20  LOAD_GLOBAL           1  'False'
          23  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 23

        self.apply_list_adapter.remove_item_by(the_filter)
