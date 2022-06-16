from PIL import Image
import chardet
import glob
import sys
import os
import re

same_hierarchy = (os.path.dirname(sys.argv[0]))#同一階層のパスを変数へ代入
#same_hierarchy = os.path.join(same_hierarchy,'ext')#debug

PSP = bool( os.path.isfile(os.path.join(same_hierarchy,'ONS.INI')) )

scenario_dir = os.path.join(same_hierarchy,'data','snr')
se_dir = os.path.join(same_hierarchy,'se')

stand_dir = os.path.join(same_hierarchy,'grp','stand')
other_dir = os.path.join(same_hierarchy,'grp','other')
parts_dir = os.path.join(same_hierarchy,'grp','parts')
gebg_dir = os.path.join(same_hierarchy,'grp','gebg')
evcg_dir = os.path.join(same_hierarchy,'grp','evcg')

effect_startnum=10
effect_list=[]

str2var_dict={}
str2var_num=[50, 50, 1000]

sel_dict={}


#--------------------def--------------------

def effect_edit(t,f):
	global effect_list

	list_num=0
	if re.fullmatch(r'[0-9]+',t):#timeが数字のみ＝本処理

		for i, e in enumerate(effect_list,effect_startnum+1):#1からだと番号が競合する可能性あり
			if (e[0] == t) and (e[1] == f):
				list_num = i

		if not list_num:
			effect_list.append([t,f])
			list_num = len(effect_list)+effect_startnum

	return str(list_num)

def str2var(s,i):
	global str2var_dict
	global str2var_num

	d=str2var_dict.get(s)

	if d:
		s2=d
	else:
		str2var_dict[s]=str2var_num[i]
		s2=str2var_num[i]
		str2var_num[i]+=1
	
	return s2


def stand_name(aaa):
	aaa = aaa.replace('うっとり','uttori')
	aaa = aaa.replace('エプロン','apron')
	aaa = aaa.replace('ネグリジェ','negligee')
	aaa = aaa.replace('下着','shitagi')
	aaa = aaa.replace('不機嫌','hukigen')
	aaa = aaa.replace('喜び','yorokobi')
	aaa = aaa.replace('困る','komaru')
	aaa = aaa.replace('嬉しい','uresii')
	aaa = aaa.replace('小夜','sayo')
	aaa = aaa.replace('怒り','ikari')
	aaa = aaa.replace('悩む','nayamu')
	aaa = aaa.replace('悲しい','kanasii')
	aaa = aaa.replace('普通','hutsuu')
	aaa = aaa.replace('私服','shihuku')
	aaa = aaa.replace('服','huku')
	aaa = aaa.replace('裸','hadaka')
	aaa = aaa.replace('輝','hikaru')
	aaa = aaa.replace('近','chikai')
	aaa = aaa.replace('遠','tooi')
	aaa = aaa.replace('香織','kaori')

	return aaa

def gebg_name(bbb):
	bbb = bbb.replace('リビング','living')
	bbb = bbb.replace('主人公部屋','shuzinkou_room')
	bbb = bbb.replace('催眠教室','saimin')
	bbb = bbb.replace('夕','yuu')
	bbb = bbb.replace('夜','yoru')
	bbb = bbb.replace('寝室','shinsitsu')
	bbb = bbb.replace('昼','hiru')
	bbb = bbb.replace('空','sora')
	bbb = bbb.replace('自宅外観','zitaku')
	bbb = bbb.replace('風呂','huro')
	bbb = bbb.replace('本屋','honya')

	return bbb


#--------------------ファイル整理--------------------

#音源リネーム
for p in  glob.glob(os.path.join(se_dir, '*')) :
	p_num = str2var((os.path.splitext(os.path.basename(p))[0]).lower(),1)
	p2 = os.path.join(os.path.dirname(p), str(p_num)+os.path.splitext(p)[1])

	os.rename(p, p2)

for p in  glob.glob(os.path.join(gebg_dir, '*')) :
	p_ren = gebg_name((os.path.splitext(os.path.basename(p))[0]).lower())
	p2 = os.path.join(os.path.dirname(p), str(p_ren)+os.path.splitext(p)[1])

	os.rename(p, p2)

for p in  glob.glob(os.path.join(stand_dir, '*')) :
	p_ren = stand_name((os.path.splitext(os.path.basename(p))[0]).lower())
	p2 = os.path.join(os.path.dirname(p), str(p_ren)+os.path.splitext(p)[1])

	os.rename(p, p2)

#--------------------0.txt作成--------------------

with open(os.path.join(same_hierarchy, 'default.txt')) as f:
	txt = f.read()

pathlist = glob.glob(os.path.join(scenario_dir, 'general', '*.snr'))
pathlist.extend(glob.glob(os.path.join(scenario_dir, '*.snr')))

for snr_path in pathlist:
	
	with open(snr_path, 'rb') as f:
		char_code =chardet.detect(f.read())['encoding']

	with open(snr_path, encoding=char_code, errors='ignore') as f:
		#memo
		txt += '\n;--------------- '+ os.path.splitext(os.path.basename(snr_path))[0] +' ---------------\nend\n\n'
		txt = txt.replace('//', ';;;')

		for line in f:
			#最初にやっとくこと
			Block_line = re.match(r'\[(.+?)\]',line)
			jump_line = re.match(r'シナリオジャンプ\("([\-A-z0-9]+?)"\)',line)
			trans_line = re.match(r'トランジション\(([0-9]+?)\)',line)
			chrmsg_line = re.match(r'【(.+?)】(\((.+?)\))?(.+?)\n',line)
			BGM_line = re.match(r'音楽再生\("([\-A-z0-9]+?)"\)',line)
			set_line = re.match('(f\.[A-z]{2}[0-9]+) ?= ?"(.+)?";', line)
			sel_line = re.match(r'選択肢実行\(([0-9]+), ([0-9]+)\)', line)
			selset_line = re.match(r'選択肢登録\(([0-9]+), "(.+?)", "(.+?)"\)', line)
			tati_line = re.match(r'前景\(f\.(.+?), f\.(.+?)\+"(.+?)"\)', line)
			haikei_line = re.match(r'背景\("(.+?)"\)', line)
			seplay_line = re.match(r'(LOOP)?効果音再生\(([0-9]), "(.+?)"\)', line)

			if re.search('^\n', line):#空行
				#line = ''#行削除
				pass#そのまま放置

			elif re.match(r'\*', line):#nsc側でラベルと勘違いするの対策
				line = r';' + line#エラー防止の為コメントアウト

			elif re.match(r'　', line):
				line = line.replace('\n','') + '\\\n'

			elif re.match(r'リターン', line):
				line = 'return\n'

			elif re.match(r'ファンクションコール\(".+?キャラOUT"\)', line):
				line = 'vsp 12,0:print 2\n'

			elif selset_line:
				sel_dict[selset_line[1]]= [selset_line[3],'*STR_'+str(str2var(selset_line[2].lower(),2))]
				line = ';処理済\t;;'+line

			elif sel_line:
				sel = 'select '
				sd1 = sel_dict[ sel_line[1] ]
				sd2 = sel_dict[ sel_line[2] ]
				sel += '"'+sd1[0]+'",'+sd1[1]+',"'+sd2[0]+'",'+sd2[1]+'"\n'
				line = sel

			elif set_line:
				if re.match(r'CC0[0-9]', (set_line[1][2:]) ) and set_line[2]:
					line='mov $'+str(str2var(set_line[1][2:].lower(),0))+',"'+stand_name(set_line[2])+'"\n'

			elif tati_line:
				line='lsp 12,"grp\\stand\\"+$'+str(str2var(tati_line[2].lower(),0))+'+"'+stand_name(tati_line[3])+'.png",0,0:print 2\n'

			elif seplay_line:
				line = ('dwave '+seplay_line[2]+',"se\\'+str(str2var(seplay_line[3].lower(),1))+'.ogg"\n')

			elif Block_line:
				if re.match(r'\[([\-A-z0-9]+?)\]',line):
					line = '*'+str(Block_line[1]).replace('-','_') + '\n'
				else:
					line = '*STR_'+str(str2var(Block_line[1].lower(),2)) + '\t;;'+Block_line[1]+'\n'


			elif jump_line:
				line = 'goto *'+str(jump_line[1]).replace('-','_') + '\n'

			elif trans_line:
				line = 'print '+ effect_edit(trans_line[1], 'fade') + '\n'

			elif chrmsg_line:
				line = r'['+chrmsg_line[1]+r']'+chrmsg_line[4] + '\\\n'

				if (chrmsg_line[3]):
					line ='dwave 10,"voice\\'+chrmsg_line[3]+'.ogg"\n'+line

			elif haikei_line:#memo:その後のprint不要
				if haikei_line[1] =='BLACK':
					line='vsp 12,0:print 2:bg black,3\n'
				elif re.match(r'EV',haikei_line[1]):
					line='vsp 12,0:print 2:bg "grp\\evcg\\'+haikei_line[1]+'.png",3\n'
				else:
					line='vsp 12,0:print 2:bg "grp\\gebg\\'+gebg_name(haikei_line[1])+'.png",3\n'

			elif BGM_line:
				line = 'bgm "bgm\\'+str(BGM_line[1])+ '.ogg"\n'


			else:#どれにも当てはまらない、よく分からない場合
				line = r';' + line#エラー防止の為コメントアウト
				#print(line)


			txt += line

if PSP:
	pathlist2 = glob.glob(os.path.join(stand_dir, '*.png'))
	pathlist2.extend(glob.glob(os.path.join(other_dir, '*.png')))
	pathlist2.extend(glob.glob(os.path.join(parts_dir, '*.png')))
	pathlist2.extend(glob.glob(os.path.join(gebg_dir, '*.png')))
	pathlist2.extend(glob.glob(os.path.join(evcg_dir, '*.png')))

	for img_path in pathlist2:
		img = Image.open(img_path)

		width, height = img.size
		width_r = width*480/1280
		height_r = height*480/1280

		if int(height_r) == 270:
			height_r = 272

		img_resize = img.resize((int(width_r), int(height_r)))
		img_resize.save(img_path)

add0txt_effect = ''
for i,e in enumerate(effect_list,effect_startnum+1):#エフェクト定義用の配列を命令文に&置換

	if e[1] == 'fade':
		add0txt_effect +='effect '+str(i)+',10,'+e[0]+'\n'

	#else:#今作フェードしか無いからこっち使わないんだよね
		#add0txt_effect +='effect '+str(i)+',18,'+e[0]+',"rule\\'+e[1]+'.png"\n'

txt = txt.replace(r';<<-EFFECT->>', add0txt_effect)

if PSP:
	txt = txt.replace(r';$V2000G200S1280,720L10000', r';$V2000G200S480,272L10000')
	txt = txt.replace(r';<<-PSP_MODE->>', r'mov %199,1')
else:
	txt = txt.replace(r';<<-PSP_MODE->>', r'mov %199,0')

open(os.path.join(same_hierarchy,'0.txt'), 'w', errors='ignore').write(txt)