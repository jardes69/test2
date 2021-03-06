from HTMLComponent import HTMLComponent
from GUIComponent import GUIComponent
from skin import parseColor, parseFont
import skin
from enigma import eListboxServiceContent, eListbox, eServiceCenter, eServiceReference, gFont, eRect
from Tools.LoadPixmap import LoadPixmap

from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN

from Tools.FindPicon import findPicon
from Tools.ServiceRecording import recordService
from Components.config import config

class ServiceList(HTMLComponent, GUIComponent):
	MODE_NORMAL = 0
	MODE_FAVOURITES = 1

	def __init__(self):
		GUIComponent.__init__(self)
		self.l = eListboxServiceContent()

		pic = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/folder.png"))
		if pic:
			self.l.setPixmap(self.l.picFolder, pic)

		pic = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/marker.png"))
		if pic:
			self.l.setPixmap(self.l.picMarker, pic)

		pic = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/icon_dvb_s.png"))
		if pic:
			self.l.setPixmap(self.l.picDVB_S, pic)

		pic = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/icon_dvb_c.png"))
		if pic:
			self.l.setPixmap(self.l.picDVB_C, pic)

		pic = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/icon_dvb_t.png"))
		if pic:
			self.l.setPixmap(self.l.picDVB_T, pic)

		pic = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/ico_service_group-fs8.png"))
		if pic:
			self.l.setPixmap(self.l.picServiceGroup, pic)

		pic =  LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/epgclock.png"))
		if pic:
			self.l.setPixmap(self.l.picRecordService, pic)

		if config.usage.servicelist_show_picon.value:
			self.l.setPiconFunction(findPicon)

		if config.usage.servicelist_mark_rec_service:
			self.l.setRECServiceFunction(recordService)

		self.picon_width = int(config.usage.servicelist_show_picon.value)
		self.custom_picon_width, self.custom_picon_height = skin.parameters.get("ServicelistCustomPiconSize", (50,30))
		self.root = None
		self.mode = self.MODE_NORMAL
		self.min_two_line_height = int(skin.parameters.get("ServicelistDoubleSpacedMinHeight", (50,))[0])
		if self.picon_width == 100:
			self.ItemHeight = 60
			p_w = 100
			p_h = 60
		elif self.picon_width == 50:
			self.ItemHeight = 30
			p_w = 50
			p_h = 30
		elif self.picon_width == 1:
			self.ItemHeight = self.custom_picon_height
			p_w = self.custom_picon_width
			p_h = self.custom_picon_height
		else:
			self.ItemHeight = 30
		if config.usage.servicelist_two_lines.value and self.ItemHeight < self.min_two_line_height:
			self.ItemHeight = self.min_two_line_height
		if self.picon_width > 0:
			self.l.setPiconHeight(int(p_h))
			self.l.setPiconWidth(int(p_w))
		self.ServiceNameFont = parseFont("Regular;22", ((1,1),(1,1)))
		self.ServiceInfoFont = parseFont("Regular;18", ((1,1),(1,1)))
		self.ServiceNumberFont = parseFont("Regular;20", ((1,1),(1,1)))
		self.onSelectionChanged = [ ]

	def applySkin(self, desktop, parent):
		attribs = [ ]
		if self.skinAttributes is not None:
			attribs = [ ]
			for (attrib, value) in self.skinAttributes:
				if attrib == "foregroundColorMarked":
					self.l.setColor(eListboxServiceContent.markedForeground, parseColor(value))
				elif attrib == "foregroundColorMarkedSelected":
					self.l.setColor(eListboxServiceContent.markedForegroundSelected, parseColor(value))
				elif attrib == "backgroundColorMarked":
					self.l.setColor(eListboxServiceContent.markedBackground, parseColor(value))
				elif attrib == "backgroundColorMarkedSelected":
					self.l.setColor(eListboxServiceContent.markedBackgroundSelected, parseColor(value))
				elif attrib == "foregroundColorServiceNotAvail":
					self.l.setColor(eListboxServiceContent.serviceNotAvail, parseColor(value))
				elif attrib == "colorEventProgressbar":
					self.l.setColor(eListboxServiceContent.serviceEventProgressbarColor, parseColor(value))
				elif attrib == "colorEventProgressbarSelected":
					self.l.setColor(eListboxServiceContent.serviceEventProgressbarColorSelected, parseColor(value))
				elif attrib == "colorEventProgressbarBorder":
					self.l.setColor(eListboxServiceContent.serviceEventProgressbarBorderColor, parseColor(value))
				elif attrib == "colorEventProgressbarBorderSelected":
					self.l.setColor(eListboxServiceContent.serviceEventProgressbarBorderColorSelected, parseColor(value))
				elif attrib == "colorServiceDescription":
					self.l.setColor(eListboxServiceContent.serviceDescriptionColor, parseColor(value))
				elif attrib == "colorServiceDescriptionSelected":
					self.l.setColor(eListboxServiceContent.serviceDescriptionColorSelected, parseColor(value))
				elif attrib == "colorServiceRecording":
					self.l.setColor(eListboxServiceContent.serviceRecordingColor, parseColor(value))
				elif attrib == "picServiceEventProgressbar":
					pic = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, value))
					if pic:
						self.l.setPixmap(self.l.picServiceEventProgressbar, pic)
				elif attrib == "serviceItemHeight":
					if self.picon_width == 0:
						self.ItemHeight = int(value)
					else:
						if self.ItemHeight < int(value):
							self.ItemHeight = int(value)
					if config.usage.servicelist_two_lines.value and self.ItemHeight < self.min_two_line_height:
						self.ItemHeight = self.min_two_line_height
				elif attrib == "serviceNameFont":
					self.ServiceNameFont = parseFont(value, ((1,1),(1,1)))
				elif attrib == "serviceInfoFont":
					self.ServiceInfoFont = parseFont(value, ((1,1),(1,1)))
				elif attrib == "serviceNumberFont":
					self.ServiceNumberFont = parseFont(value, ((1,1),(1,1)))
				elif attrib == "progressbarHeight":
					self.l.setProgressbarHeight(int(value))
				elif attrib == "progressbarBorderWidth":
					self.l.setProgressbarBorderWidth(int(value))
				else:
					attribs.append((attrib, value))
		self.skinAttributes = attribs
		return GUIComponent.applySkin(self, desktop, parent)

	def connectSelChanged(self, fnc):
		if not fnc in self.onSelectionChanged:
			self.onSelectionChanged.append(fnc)

	def disconnectSelChanged(self, fnc):
		if fnc in self.onSelectionChanged:
			self.onSelectionChanged.remove(fnc)

	def selectionChanged(self):
		for x in self.onSelectionChanged:
			x()

	def setCurrent(self, ref):
		self.l.setCurrent(ref)

	def getCurrent(self):
		r = eServiceReference()
		self.l.getCurrent(r)
		return r

	def atBegin(self):
		return self.instance.atBegin()

	def atEnd(self):
		return self.instance.atEnd()

	def moveUp(self):
		self.instance.moveSelection(self.instance.moveUp)

	def moveDown(self):
		self.instance.moveSelection(self.instance.moveDown)

	def moveToChar(self, char):
		# TODO fill with life
		print "Next char: "
		index = self.l.getNextBeginningWithChar(char)
		indexup = self.l.getNextBeginningWithChar(char.upper())
		if indexup != 0:
			if (index > indexup or index == 0):
				index = indexup

		self.instance.moveSelectionTo(index)
		print "Moving to character " + str(char)

	def moveToNextMarker(self):
		idx = self.l.getNextMarkerPos()
		self.instance.moveSelectionTo(idx)

	def moveToPrevMarker(self):
		idx = self.l.getPrevMarkerPos()
		self.instance.moveSelectionTo(idx)

	def moveToIndex(self, index):
		self.instance.moveSelectionTo(index)

	def getCurrentIndex(self):
		return self.instance.getCurrentIndex()

	GUI_WIDGET = eListbox
	
	def postWidgetCreate(self, instance):
		instance.setWrapAround(True)
		instance.setContent(self.l)
		instance.selectionChanged.get().append(self.selectionChanged)
		self.setMode(self.mode)

	def preWidgetRemove(self, instance):
		instance.setContent(None)
		instance.selectionChanged.get().remove(self.selectionChanged)

	def getRoot(self):
		return self.root

	def getRootServices(self):
		serviceHandler = eServiceCenter.getInstance()
		list = serviceHandler.list(self.root)
		dest = [ ]
		if list is not None:
			while 1:
				s = list.getNext()
				if s.valid():
					dest.append(s.toString())
				else:
					break
		return dest

	def setNumberOffset(self, offset):
		self.l.setNumberOffset(offset)

	def setPlayableIgnoreService(self, ref):
		self.l.setIgnoreService(ref)

	def setRoot(self, root, justSet=False):
		self.root = root
		self.l.setRoot(root, justSet)
		if not justSet:
			self.l.sort()
		self.selectionChanged()
		
	def setPythonConfig(self):
		self.l.setPythonConfig()

	def removeCurrent(self):
		self.l.removeCurrent()

	def addService(self, service, beforeCurrent=False):
		self.l.addService(service, beforeCurrent)

	def finishFill(self):
		self.l.FillFinished()
		self.l.sort()

# stuff for multiple marks (edit mode / later multiepg)
	def clearMarks(self):
		self.l.initMarked()

	def isMarked(self, ref):
		return self.l.isMarked(ref)

	def addMarked(self, ref):
		self.l.addMarked(ref)

	def removeMarked(self, ref):
		self.l.removeMarked(ref)

	def getMarked(self):
		i = self.l
		i.markedQueryStart()
		ref = eServiceReference()
		marked = [ ]
		while i.markedQueryNext(ref) == 0:
			marked.append(ref.toString())
			ref = eServiceReference()
		return marked

#just for movemode.. only one marked entry..
	def setCurrentMarked(self, state):
		self.l.setCurrentMarked(state)

	def setMode(self, mode):
		self.mode = mode
		picon_width = 0
		picon_height = 0
		picon_x_offset = int(skin.parameters.get("ServicelistPiconXOffset", (8,))[0])
		if self.picon_width == 1:
			picon_width = self.custom_picon_width + picon_x_offset
			picon_height = self.custom_picon_height
		elif self.picon_width > 1:
			picon_width = self.picon_width + picon_x_offset
			if self.picon_width == 100:
				picon_height = 60
			else:
				picon_height = 30
		service_number_offset = 0
		if config.usage.servicelist_show_servicenumber.value:
			service_number_offset = int(skin.parameters.get("ServicelistServiceNumberOffset", (60,))[0])
		if mode == self.MODE_NORMAL:
			service_number_offset = int(skin.parameters.get("ServicelistServiceNumberOffsetNormal", (0,))[0])
		progress_bar_offset = int(skin.parameters.get("ServicelistProgressbarDefaultOffset", (0,))[0])
		if config.usage.show_event_progress_in_servicelist.value:
			progress_bar_offset = int(skin.parameters.get("ServicelistProgressbarOffset", (60,))[0])
		service_type_pix_offset = 0
		if config.usage.servicelist_show_service_type_icon.value:
			service_type_pix_offset = int(skin.parameters.get("ServicelistServiceTypePixOffset", (38,))[0])
		self.l.setItemHeight(self.ItemHeight)
		self.l.setVisualMode(eListboxServiceContent.visModeComplex)
		if config.usage.servicelist_two_lines.value:
			service_number_offset_y = 0
			if config.usage.servicelist_show_next_event.value and config.usage.show_event_progress_in_servicelist.value:
				service_number_offset_y = self.ItemHeight/2
			if config.usage.servicelist_show_next_event.value:
				service_name = self.l.celServiceInfo
				service_info = self.l.celNextEventInfo
			else:
				service_name = self.l.celServiceName
				service_info = self.l.celServiceInfo
			offset = service_number_offset + progress_bar_offset
			if offset > 60:
				offset = int(skin.parameters.get("ServicelistOffset", (60,))[0])
			x,y,w,h = skin.parameters.get("Servicelist100Picon", (0, 0, picon_width, picon_height))
			self.l.setElementPosition(self.l.celPiconPixmap, eRect(x, y, w, h))
			if config.usage.servicelist_show_service_type_icon.value:
				x,y,w,h = skin.parameters.get("ServicelistServiceTypePixmap100", (0, 0, 30, 30))
				self.l.setElementPosition(self.l.celServiceTypePixmap, eRect(picon_width + offset + x, y, w, h))
			x,y,w,h = skin.parameters.get("ServicelistServiceEventProgressbar100", (0, 0, 52, 0))
			self.l.setElementPosition(self.l.celServiceEventProgressbar, eRect(picon_width + x, y, w, self.ItemHeight + h))
			if config.usage.servicelist_show_servicenumber.value and mode == self.MODE_FAVOURITES:
				self.l.setElementFont(self.l.celServiceNumber, self.ServiceNumberFont)
				x,y,w,h = skin.parameters.get("ServicelistServiceNumber100", (0, 0, 50, 0))
				self.l.setElementPosition(self.l.celServiceNumber, eRect(picon_width + x, service_number_offset_y + y, w, self.ItemHeight + h))
			x,y,w,h = skin.parameters.get("ServicelistRecordServicePixmap100", (0, 0, 30, 30))
			self.l.setElementPosition(self.l.celRecordServicePixmap, eRect(picon_width + offset + service_type_pix_offset + x, y, w, h))
			self.l.setElementFont(service_name, self.ServiceNameFont)
			x,y,w,h = skin.parameters.get("ServicelistServiceName100", (0, 0, self.instance.size().width(), 0))
			self.l.setElementPosition(service_name, eRect(picon_width + offset + service_type_pix_offset+x,y,w - offset, self.ItemHeight/2 + h))
			self.l.setElementFont(service_info, self.ServiceInfoFont)
			x,y,w,h = skin.parameters.get("ServicelistServiceInfo100", (0, 0, self.instance.size().width(), 0))
			self.l.setElementPosition(service_info, eRect(picon_width + offset + service_type_pix_offset + x, self.ItemHeight / 2 + y, w - offset, self.ItemHeight / 2 + h))
		else:
			if picon_width > 0:
				self.l.setElementPosition(self.l.celPiconPixmap, eRect(0, 0, picon_width, picon_height))
			if config.usage.servicelist_show_service_type_icon.value:
				self.l.setElementPosition(self.l.celServiceTypePixmap, eRect(picon_width + service_number_offset, 0, 30, 30))
			if service_number_offset:
				x,y,w,h = skin.parameters.get("ServicelistServiceNumber", (0, 0, 50, 0))
				self.l.setElementFont(self.l.celServiceNumber, self.ServiceNumberFont)
				self.l.setElementPosition(self.l.celServiceNumber, eRect(picon_width + x, y, w, self.ItemHeight + h))
			x,y,w,h = skin.parameters.get("ServicelistServiceEventProgressbar", (0, 0, 52, 0))
			self.l.setElementPosition(self.l.celServiceEventProgressbar, eRect(picon_width + service_number_offset + service_type_pix_offset + x, y, w, self.ItemHeight + h))
			x,y,w,h = skin.parameters.get("ServicelistRecordServicePixmap", (0, 0, 30, 30))
			self.l.setElementPosition(self.l.celRecordServicePixmap, eRect(picon_width + service_number_offset + service_type_pix_offset + progress_bar_offset + x, y, w, h))
			self.l.setElementFont(self.l.celServiceName, self.ServiceNameFont)
			x,y,w,h = skin.parameters.get("ServicelistServiceName", (0, 0, self.instance.size().width(), 0))
			self.l.setElementPosition(self.l.celServiceName, eRect(picon_width + service_number_offset + service_type_pix_offset + x, y, w - service_number_offset, self.ItemHeight + h))
			self.l.setElementFont(self.l.celServiceInfo, self.ServiceInfoFont)
			self.l.setElementFont(self.l.celServiceTime, self.ServiceInfoFont)
