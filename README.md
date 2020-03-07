# Portrait Mating  implementation in UNet with PyTorch.

**Segmentation Demo Result:**
![Segmentation](https://user-images.githubusercontent.com/30276789/76141416-03521900-609f-11ea-95e7-80d7ecf83760.png)
**Matting Demo Result:**
![Matting](https://user-images.githubusercontent.com/30276789/76142315-81b2b900-60a7-11ea-934d-35a00e50eda2.png)
For the convenience of demonstration, I built the API service through Flask, and finally deployed it on WeChat Mini Program.
The code part of the WeChat applet is in here [portrait-matting-wechat](https://github.com/leijue222/portrait-matting-wechat).

## Dependencies

- Python 3.6
- PyTorch >= 1.1.0
- Torchvision >= 0.3.0
- Flask 1.1.1
- future 0.18.2
- matplotlib 3.1.3
- numpy 1.16.0
- Pillow 6.2.0
- protobuf 3.11.3
- tensorboard 1.14.0
- tqdm==4.42.1

## Data
This model was trained from scratch with 18000 images (data augmentation by 2000images)
Training dataset was from [Deep Automatic Portrait Matting](http://www.cse.cuhk.edu.hk/leojia/projects/automatting/index.html).
Your can download in baidu cloud [http://pan.baidu.com/s/1dE14537](http://pan.baidu.com/s/1dE14537). Password: ndg8 
**For academic communication only, if there is a quote, please inform the original author!**

We augment the number of images by perturbing them withrotation and scaling. Four rotation angles{−45◦,−22◦,22◦,45◦}and four scales{0.6,0.8,1.2,1.5}are used. We also apply four different Gamma transforms toincrease color variation. The Gamma values are{0.5,0.8,1.2,1.5}. After thesetransforms, we have 18K training images. 

## Run locally
**Note : Use Python 3**
### Prediction

You can easily test the output masks on your images via the CLI.

To predict a single image and save it:

```bash
$ python predict.py -i image.jpg -o output.jpg
```

To predict a multiple images and show them without saving them:

```bash
$ python predict.py -i image1.jpg image2.jpg --viz --no-save
```

```shell script
> python predict.py -h
usage: predict.py [-h] [--model FILE] --input INPUT [INPUT ...]
                  [--output INPUT [INPUT ...]] [--viz] [--no-save]
                  [--mask-threshold MASK_THRESHOLD] [--scale SCALE]

Predict masks from input images

optional arguments:
  -h, --help            show this help message and exit
  --model FILE, -m FILE
                        Specify the file in which the model is stored
                        (default: MODEL.pth)
  --input INPUT [INPUT ...], -i INPUT [INPUT ...]
                        filenames of input images (default: None)
  --output INPUT [INPUT ...], -o INPUT [INPUT ...]
                        Filenames of ouput images (default: None)
  --viz, -v             Visualize the images as they are processed (default:
                        False)
  --no-save, -n         Do not save the output masks (default: False)
  --mask-threshold MASK_THRESHOLD, -t MASK_THRESHOLD
                        Minimum probability value to consider a mask pixel
                        white (default: 0.5)
  --scale SCALE, -s SCALE
                        Scale factor for the input images (default: 0.5)
```
You can specify which model file to use with `--model MODEL.pth`.

### Training

```shell script
> python train.py -h
usage: train.py [-h] [-e E] [-b [B]] [-l [LR]] [-f LOAD] [-s SCALE] [-v VAL]

Train the UNet on images and target masks

optional arguments:
  -h, --help            show this help message and exit
  -e E, --epochs E      Number of epochs (default: 5)
  -b [B], --batch-size [B]
                        Batch size (default: 1)
  -l [LR], --learning-rate [LR]
                        Learning rate (default: 0.1)
  -f LOAD, --load LOAD  Load model from a .pth file (default: False)
  -s SCALE, --scale SCALE
                        Downscaling factor of the images (default: 0.5)
  -v VAL, --validation VAL
                        Percent of the data that is used as validation (0-100)
                        (default: 10.0)

```
By default, the `scale` is 0.5, so if you wish to obtain better results (but use more memory), set it to 1.

The input images and target masks should be in the `data/imgs` and `data/masks` folders respectively.

### Start API service


```bash
$ python app.py
```

Then you can use the model through the API

## Run on server
1. Install virtual environment
2. Install gunicorn in a virtual environment
3. Proxy through nginx

## Notes on memory
```bash
$ python train.py -e 200 -b 1 -l 0.1 -s 0.5 -v 15.0
```
The model has be trained from scratch on a RTX2080Ti 11GB.
18,000 training dataset, running for 4 days +

## Thanks

The birth of this project is inseparable from the following projects:

- **[Flask](https://github.com/pallets/flask)：The Python micro framework for building web applications**
- **[Pytorch-UNet](https://github.com/milesial/Pytorch-UNet)：PyTorch implementation of the U-Net for image semantic segmentation with high quality images**

---

