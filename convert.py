import os, json, shutil
from datetime import datetime

# creates a string from the post date
def date_to_title(date):
    datetime_object = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
    formatted_date = datetime_object.strftime("%B %d, %Y")

    return formatted_date

# creates a string from the post date used for order posts in the frontmatter
def date_to_frontmatter(date):
    datetime_object = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
    formatted_date = datetime_object.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_date

## Instagram image file names are extremely long, this function renames the image
def rename_image(date, image, post_image_dir, inc):
    fname = date.replace(' ','_')
    ext = '-' + str(inc) + '.webp'
    fname = fname.replace(',','') + ext
    image_name = image.split('/')[4:]
    image_name = image_name[0]
    shutil.copy(image, post_image_dir)
    source_image_path = os.path.join(post_image_dir, image_name )
    dest_image_path = os.path.join(post_image_dir, fname)
    os.rename(source_image_path, dest_image_path)

    return dest_image_path

# creates the text for index.md
def create_post_text(title_date, frontmatter_date, post_images, text):
    images = []
    for i in post_images:
        image_path = i.split('/')[3:]
        image_path.insert(0,'./')
        local_path = os.path.join(*image_path)
        images.append(f'![]({local_path})')
    
    post_images = ' '.join(i for i in images)    
    content = f"""---\ntitle: {title_date}\ndate: {frontmatter_date}\n---\n
{post_images}\n\n
{text}"""

    return content

# copies and renames Hugo post images 
def create_post_images(image_src_list, post_image_dir):
    post_image_list = []
    inc = 0
    for i in image_src_list:
        post_image = rename_image(title_date, i, post_image_dir, inc)
        post_image_list.append(post_image)
        inc += 1

    return post_image_list

# created directories for Hugo posts
def create_post_dir(title_date):
    post_dir = title_date.replace(' ','_')
    post_dir = post_dir.replace(',','')
    post_dir_list = os.listdir(base_dir)
    matches = [dir for dir in post_dir_list if post_dir in dir]
    if len(matches) == 0:
        dir_path = os.path.join(base_dir, post_dir)
    elif len(matches) == 1:
        dir_path = os.path.join(base_dir, post_dir + '-1')
    else:
        dir = matches[0]
        post_cnt = dir.split('-')
        post_cnt = int(post_cnt[1])+1
        dir_path  = os.path.join(base_dir, post_dir + '-' + str(post_cnt))
    
    return dir_path

# creates the post directory, post, and post images
def create_post(title_date, frontmatter_date, image_src_list, text):
    post_dir = create_post_dir(title_date)
    post_path = os.path.join(post_dir, "index.md")
    post_image_dir = os.path.join(post_dir, "images")
    os.mkdir(post_dir)
    os.mkdir(post_image_dir)
    
    # create list of images for post
    post_images = create_post_images(image_src_list, post_image_dir)

    content = create_post_text(title_date, frontmatter_date, post_images, text)
    f = open(post_path, 'w')
    f.write(content)
    f.close()
    
    return True

base_dir = './posts/'
src = os.path.join(os.getcwd, "media") 
dest = os.path.join(os.getcwd, "posts")

f = open('posts_1.json')
data = json.load(f) 

for index, obj in enumerate(data):
    text = data[index]['media'][0]['title']
    timestamp = data[index]['media'][0]['creation_timestamp']
    title_date = date_to_title(datetime.fromtimestamp(timestamp))
    frontmatter_date = date_to_frontmatter(datetime.fromtimestamp(timestamp))
    media_list = data[index]['media']
    image_count = len(media_list) 
    image_list = []
    if image_count > 0:
        for i in range(image_count):
            path = os.path.join('./', data[index]['media'][i]['uri'])
            image_list.append(path)
    post = create_post(title_date, frontmatter_date, image_list, text )