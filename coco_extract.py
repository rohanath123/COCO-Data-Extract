from pycocotools.coco import COCO
import requests
import json

class extractCOCO:
  def __init__(self, version):
    self.version = version
    versions = {'2017':'/content/drive/My Drive/instances_train2017.json', '2014':''}
    self.coco = COCO(versions[version])
  
  def get_object_images(self, class_name):
    self.catIds = self.coco.getCatIds(catNms=[class_name])
    imgIds = self.coco.getImgIds(catIds=catIds)
    images = self.coco.loadImgs(imgIds)

    return images
  
  def download_and_save_data(self, object_classes, PATH):
    for obj in object_classes:
      img_save_PATH = PATH+obj+'/coco_'+self.version+'/images/'
      anno_save_PATH = PATH+obj+'/coco_'+self.version+'/annotations/'
      images = self.get_object_images(obj)
      print("Class "+obj+" has "+str(len(images))+" images.")
      for image in images:
        img_data = requests.get(image['coco_url']).content
        annIds = coco.getAnnIds(imgIds = image['id'], catIds = self.catIds, iscrowd=None)
        annos = coco.loadAnns(annIds)

        with open(img_save_PATH+str(image['file_name'].split('.jpg')[0])+'.png', 'wb') as f:
          f.write(img_data)

        with open(anno_save_PATH+str(image['file_name'].split('.jpg')[0])+'.json', 'w') as f:
          f.write(json.dumps(annos))
      print("Saved data for Class "+obj)
    print("Done")