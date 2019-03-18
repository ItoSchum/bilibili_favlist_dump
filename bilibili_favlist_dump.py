#!/usr/bin/python3
import os
import json
import requests
import pathlib
# import ffmpeg

# f_cookies = open(r"./myBilibiliCookies.txt","r")
# cookies = f_cookies.read()
# f_cookies.close()

# headers = {
#     'Accept':'application/json, text/plain, text/plain;charset=UTF-8, */*',
# #     'Accept-Encoding':'gzip, deflate, br',
# #     'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
# #     'Connection':'keep-alive',
#     'Cookie': cookies,
# #     'Host':'space.bilibili.com',
# #     'Origin':'https://space.bilibili.com',
# #     'Referer':'https://space.bilibili.com/uid/favlist?fid=',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
# }       

prefix = 'https://api.bilibili.com/medialist/gateway/base/'

def all_info_dump():
	mid = input('User ID (aka uid/mid): ')

	medialist_brief_jsonp = prefix + 'created?pn=1&ps=100&up_mid=' + str(mid) + '&is_space=0&jsonp=jsonp'

	medialist_brief_jsonp_raw = requests.get(medialist_brief_jsonp).text
	wdata = json.loads(medialist_brief_jsonp_raw)
	medialist_count = wdata['data']['count']
	medialist = wdata['data']['list']

	medialist_brief = []
	# medialist_brief.clear()
	print("")
	print("%-8s %-6s %s" % ('FID', 'Amount', 'Favlist Title'))
	for favlist_item in medialist:    
		fid = favlist_item['id']    
		title = favlist_item['title']    
		media_count = favlist_item['media_count']
		medialist_brief.append({'fid': fid, 'title': title, 'media_count': media_count})	
		print("%-8s %-6s %s" % (fid, media_count, title))
	print("")

	# Each individual medialist
	medialist_detail = []
	for i in range(len(medialist_brief)):
		medialist_detail.append([])

	for serial in range(0, medialist_count, 1):
		print("Favlist: %-8s %-s" % (medialist_brief[serial]['fid'], medialist_brief[serial]['title']))
		fid = medialist_brief[serial]['fid']
		
		if medialist_brief[serial]['media_count'] % 20 != 0:
			page_num_max = int(medialist_brief[serial]['media_count'] / 20) + 1
		else:
			page_num_max = int(medialist_brief[serial]['media_count'] / 20)

		for page_num in range(1, page_num_max + 1, 1):
			medialist_detail_jsonp = prefix + 'spaceDetail?media_id=' + str(fid) +'&pn=' + str(page_num) +'&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'
			medialist_detail_raw = requests.get(medialist_detail_jsonp).text
			wdata = json.loads(medialist_detail_raw)
			medias = wdata['data']['medias']
			
			print("Page %02d" % (page_num))
			for media_item in medias:    
				media_item_detail = media_item_detail_dump(media_item)
				medialist_detail[serial].append(media_item_detail)
			print("")

		medialist_detail_dump(medialist_detail[serial], medialist_brief[serial]['title'])

	return (medialist_detail, medialist_brief)



def single_info_dump():
	fid = input('Medialist ID (aka fid): ')

	medialist_detail_jsonp = prefix + 'spaceDetail?media_id=' + str(fid) +'&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'
	medialist_detail_raw = requests.get(medialist_detail_jsonp).text
	wdata = json.loads(medialist_detail_raw)
	
	media_count = wdata['data']['info']['media_count']
	medialist_fid = wdata['data']['info']['fid']
	medialist_title = wdata['data']['info']['title']

	print("")
	print("%-8s %-6s %s" % ('FID', 'Amount', 'Favlist Title'))
	print("%-8s %-6s %s" % (medialist_fid, media_count, medialist_title))
	print("")

	if media_count != 0:
		page_num_max = int(media_count / 20) + 1
	else:
		page_num_max = int(media_count / 20)

	medialist_detail = []
	for page_num in range(1, page_num_max + 1, 1):
		medialist_detail_jsonp = prefix + 'spaceDetail?media_id=' + str(fid) +'&pn=' + str(page_num) +'&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'
		medialist_detail_raw = requests.get(medialist_detail_jsonp).text
		wdata = json.loads(medialist_detail_raw)
		medias = wdata['data']['medias']
			
		print("Page %02d" % (page_num))
		for media_item in medias:    
			media_item_detail = media_item_detail_dump(media_item)
			medialist_detail.append(media_item_detail)
		print("")

	medialist_detail_dump(medialist_detail, medialist_title)
		
	return (medialist_detail, medialist_title)


def media_item_detail_dump(media_item):
	invalid = "已失效视频"

	media_id = media_item['id']    
	title = media_item['title']
	media_page_num = int(media_item['page'])
	sub_titles = []
	if title != invalid:
		for page in media_item['pages']:
			sub_titles.append(page['title'])
			# print(page['title'])
	# intro = media_item['intro'] 
	upper_mid = media_item['upper']['mid']
	upper_name = media_item['upper']['name']
	print(media_id, upper_name, title)
	
	media_item_detail = {'media_id': media_id, 'title': title, 'upper_mid': upper_mid, 'upper_name': upper_name, 'sub_titles': sub_titles, 'media_page_num': media_page_num}
	return media_item_detail


def medialist_detail_dump(medialist_detail, medialist_title):
	media_page_sum = 0
	valid_sum = 0
	invalid = "已失效视频"

	o_metadata=open(r"favlist_" + medialist_title + ".csv", "w", encoding='utf-8')
	print("Media_ID, Upper_ID, Upper_Name, Title", file = o_metadata)
	
	for i in range(len(medialist_detail)):
		print('av"%s", "%s", "%s", "%s"' % (medialist_detail[i]['media_id'], medialist_detail[i]['upper_mid'], medialist_detail[i]['upper_name'], medialist_detail[i]['title']), file = o_metadata)
		media_page_sum += medialist_detail[i]['media_page_num']
		if medialist_detail[i]['title'] != invalid:
			valid_sum += medialist_detail[i]['media_page_num']

	ps = "PS: Single Media_ID may contain multiple videos."
	print("\n")
	print("Media_Amount, Valid_Amount", file = o_metadata)
	print('"%s", "%s", "%s"' % (media_page_sum, valid_sum, ps), file = o_metadata)
	
	print("Media Amount: %s" % (media_page_sum))
	print("Valid Amount: %s" % (valid_sum))
	print("PS: single Media_ID may contain multiple videos.")

	print("\nDONE. Metadata file has been created in your current directory.")
	o_metadata.close()


def file_dump(item_list, dump_mode, cookie_path, output_path, title = ""):

	# f_cookies = open(r"./myBilibiliCookies.txt","r")
	# cookies = f_cookies.read()
	# f_cookies.close()

	favlist_title = "favlist_" + title + ".csv"
	os.system('mv "%s" "%s"' % (favlist_title, output_path))
	output_path = os.path.join(os.path.expanduser(output_path), title)
	mkdir(output_path) 
	
	thread_amount = 15

	for media_item in item_list: 
		folder_basename = media_item['upper_name']
		folder_path = os.path.join(os.path.expanduser(output_path), folder_basename)
		mkdir(folder_path)

		part_num = 0
		for sub_title in media_item['sub_titles']:
			part_num += 1
			
			if sub_title != "":	
				target = media_item['title'] + " " + sub_title
				if len(target) > 80:
					target = media_item['title'] + " P" + str(part_num) + " " + sub_title
					target = target[0:77] + "..."
			else:
				target = media_item['title']
				if len(target) > 80:
					target = target[0:77] + "..."

			target_flv = target + ".flv"
			target_mp4 = target + ".mp4"
			
			target_fuzzy = target.split('...')[0]
			target_fuzzy = target_fuzzy.replace("'", "’")
			target_fuzzy = target_fuzzy.replace("/", " ")
			target_fuzzy = target_fuzzy.replace("┗|", "┗-")
			target_fuzzy = target_fuzzy.replace("|┓", "-┓")
			target_fuzzy = target_fuzzy.replace(": ", "：")
			target_fuzzy = target_fuzzy.replace("★|", "★-")

			target_fuzzy_flv = target_fuzzy + ".flv"
			target_fuzzy_mp4 = target_fuzzy + ".mp4"
			
			# path_flv = pathlib.Path(os.path.join(os.path.expanduser(folder_path), target_flv))
			# path_mp4 = pathlib.Path(os.path.join(os.path.expanduser(folder_path), target_mp4))
			# print("CURRENT: " + target_flv)
			# print("CURRENT TARGET: " + os.path.join(os.path.expanduser(folder_path), target_flv))
			
			target_exist_check = False
			exist_files = os.listdir(os.path.join(os.path.expanduser(folder_path) ) )
			# print("TARGET: " + target_fuzzy + "(.flv/.mp4)")
			for file in exist_files:
				# print("EXIST:  " + file.split('...')[0]) 
				if (target_fuzzy_flv == file or target_fuzzy_mp4 == file):
					target_exist_check = True
					break
				elif target_fuzzy == file.split('...')[0]:
					target_exist_check = True
					break
				elif "活动作品" in file:
					target_fuzzy == file.split("活动作品")[1]
					target_exist_check = True
					break

			# if (path_flv.exists() or path_mp4.exists()):
			# 	target_exist_check = True

			if target_exist_check == True:
				print("--- FILE Already Exists --- " + target_fuzzy + "(.flv/.mp4)")

			else:
				if cookie_path == '0':
					os.system('annie -n %d -o "%s" -p av%d' % (thread_amount, folder_path, media_item['media_id']))
				else:
					os.system('annie -n %d -c "%s" -o "%s" -p av%d' % (thread_amount, cookie_path, folder_path, media_item['media_id']))
				# ffmpeg_repack(folder_path, media_item['title'])
				print("--- DOWNLOAD COMPLETE --- " + target + "(.flv/.mp4)")
			
				
			

# def ffmpeg_repack(folder_path, title):
# 	media_basename = os.path.join(os.path.expanduser(folder_path), title)
# 	media_input = media_basename + '.flv'
# 	media_output = media_basename + '.mp4'
# 	stream = ffmpeg.input(media_input)
# 	stream = ffmpeg.output(stream, media_output, **{'c': 'copy', 'movflags': '+faststart'})
# 	ffmpeg.run(stream)



def mkdir(path):
	
	folder = os.path.exists(path)
	if not folder:                   
		os.makedirs(path)            
		print("---  MADE NEW DIR  ---")
	else:
		print("---  DIR Already Exists  ---")



def __main__():
	dump_mode = input("\nPlease Choose Mode:\n 1 --- Dump Single Favlist\n 2 --- Dump All\n 3 --- Dump Single Favlist Info\n 4 --- Dump All Favlist Info\nMode: ")

	if dump_mode == '1':
		cookie_path = input('Cookie Path (0 for not required): ')
		output_path = input('Output Path: ')

		medialist_info_set = single_info_dump()
		medialist_detail = medialist_info_set[0]
		medialist_title = medialist_info_set[1]
		file_dump(medialist_detail, dump_mode, cookie_path, output_path, title = medialist_title)
	
	elif dump_mode == '2':
		cookie_path = input('Cookie Path (0 for not required): ')
		output_path = input('Output Path: ')

		medialist_info_set = all_info_dump()
		medialist_detail = medialist_info_set[0]
		medialist_brief = medialist_info_set[1]
		serial = 0
		for medialist in medialist_detail: 
			title = medialist_brief[serial]['title']
			file_dump(medialist_detail[serial], dump_mode, cookie_path, output_path, title = title)
			serial += 1

	elif dump_mode == '3':
		medialist_info_set = single_info_dump()

	elif dump_mode == '4':
		medialist_detail = all_info_dump()

	print('\nALL COMPLETE')

__main__()





