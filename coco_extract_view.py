from pycocotools.coco import COCO
import requests
import json
import cv2 

class extractCOCO:
  def __init__(self, version):
    self.version = version
    versions = {'2017':'/content/drive/My Drive/COCO Annotation Files/instances_train2017.json', '2017_val': '/content/drive/My Drive/COCO Annotation Files/instances_val2017.json'}
    self.coco = COCO(versions[version])
  
  def get_object_images(self, class_name):
    self.catIds = self.coco.getCatIds(catNms=[class_name])
    imgIds = self.coco.getImgIds(catIds=self.catIds)
    images = self.coco.loadImgs(imgIds)

    return images
  
  def download_and_save_data(self, object_classes, count):
    for obj in object_classes:
      img_save_PATH = '/content/drive/My Drive/COCO Annotation Files/coco_view_images/images/'+obj+'/'
      anno_save_PATH = '/content/drive/My Drive/COCO Annotation Files/coco_view_images/annotations/'+obj+'/'

      images = self.get_object_images(obj)

      print("Class "+obj+" has "+str(len(images))+" images.")

      i = 0
      
      for image in images:
        img_data = requests.get(image['coco_url']).content
        annIds = self.coco.getAnnIds(imgIds = image['id'], catIds = self.catIds, iscrowd=None)
        annos = self.coco.loadAnns(annIds)

        with open(img_save_PATH+str(image['file_name'].split('.jpg')[0])+'.png', 'wb') as f:
          f.write(img_data)

        img = cv2.imread(img_save_PATH+str(image['file_name'].split('.jpg')[0])+'.png')
        
        for ann in annos:
          x1, y1, w, h = int(ann['bbox'][0]), int(ann['bbox'][1]), int(ann['bbox'][2]), int(ann['bbox'][3])
          cv2.rectangle(img, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), thickness=2)
        
        cv2.imwrite(img_save_PATH+str(image['file_name'].split('.jpg')[0])+'.png', img)
        print("Image Number: "+str(i))
        i = i+1
        if i == count:
          break
      print("Saved data for Class "+obj)
    print("Done")