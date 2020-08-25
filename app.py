import sys
import os
from flask import Flask, render_template, request, jsonify, send_file, make_response
import youtube_dl as ytd
import shutil
from flask_apscheduler import APScheduler


app = Flask(__name__)
scheduler = APScheduler()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
	link = request.form['link']
	print(link)
	if "playlist" in link or "list" in link:
		outtmpl = 'media/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'
		params ={
			'format': 'bestaudio/best',
			'outtmpl': outtmpl,
			'postprocessors':[{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
		}
		yt = ytd.YoutubeDL(params)
		info_dict = yt.extract_info(link, download=True)
		video_title = info_dict.get('title', None)
		title = video_title.replace('"', r"'")
		# video_id = info_dict.get("id", None)
		name = 'media/'+video_title
		shutil.make_archive(name, zip, name)
		os.rmdir(name)
		vt = title+'.zip'
		return jsonify({'download' : vt})

	else:
		outtmpl = 'media/%(title)s.%(ext)s'
		params ={
			'format': 'bestaudio/best',
			'outtmpl': outtmpl,
			'postprocessors':[{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
		}
		yt = ytd.YoutubeDL(params)
		info_dict = yt.extract_info(link, download=True)
		video_title = info_dict.get('title', None)
		title = video_title.replace('"', r"'")
		# video_id = info_dict.get("id", None)
		vt = title+'.mp3'
		return jsonify({'download' : vt})

	return jsonify({'nothing': 'nothing here'})

@app.route('/download/<filename>')
def download(filename):
	fn='media/'+filename
	return send_file(fn, as_attachment=True)



def delete():
	for root, dirs, files in os.walk('media'):
		for f in files:
			os.remove(os.path.join(root, f))
		for d in dirs:
			shutil.rmtree(os.path.join(root, d))


if __name__ == '__main__':
	scheduler.add_job(id='delete task', func=delete, trigger='interval', seconds=3600)
	scheduler.start()
	app.run(debug=True, threaded=True)
