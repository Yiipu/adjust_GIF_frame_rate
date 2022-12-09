import glob
from shutil import rmtree
import os
from PIL import Image, ImageSequence

def extract_png_frames(gif_file, output_dir,pick_rate):
    gif = Image.open(gif_file)
    os.makedirs(output_dir, exist_ok=True)
    for i, frame in enumerate(ImageSequence.Iterator(gif)):
        if i%pick_rate==0:
            frame.save(f'{output_dir}/{int(i/pick_rate)}.png', 'PNG')
    return int(i/pick_rate)

def create_gif(png_frames, output_file, duration):
    png_frames = [Image.open(frame) for frame in png_frames]
    png_gif = png_frames[0].save(
        output_file,
        'GIF',
        save_all=True,
        append_images=png_frames[1:],
        duration=duration,
        disposal=2,
        loop=0
    )

def main():
    gif_files = glob.glob('*.gif')
    
    new_frame_rate = int(input(
        '输入调整后的帧率：'))

    for file in gif_files:
        gif = Image.open(file)
        origin_duration=gif.info['duration']
        origin_frame_rate=int(1000/origin_duration)
        pick_rate=int(origin_frame_rate/new_frame_rate)
        new_duration=pick_rate*origin_duration
        
        print(f'{file} 帧率为 {origin_frame_rate}，每 {pick_rate} 帧选一帧，持续 {new_duration} ms')
        
        frame_num=extract_png_frames(file, f'frames/{file}',pick_rate)
        print(frame_num)

        png_frames = [f'frames/{file}/{i}.png'
                      for i in range(frame_num)]
        create_gif(png_frames, f'output/{file}', new_duration)

    response = input('保存提取的帧吗？（Y/N）')
    if response.lower() not in ('yes', 'y'):
        rmtree(f'frames')

if __name__ == '__main__':
    main()
