import numpy as np
import sys
import requests
import os
import zipfile
from clint.textui import progress
import pandas as pd

#function to download file from url with progress bar and save to fn
def download_file(url, fn):
  #if prices paid data doesn't exist, download it
  resp = requests.get(url, stream=True)
  with open(fn, 'wb') as f:
    total_length = int(resp.headers.get('content-length'))
    for chunk in progress.bar(resp.iter_content(chunk_size=1024), expected_size=(total_length/1024)+1):
      if chunk:
        f.write(chunk)
        f.flush()

#urls and filenames
data_fldr = 'data'
if not os.path.exists(data_fldr):
  os.mkdir(data_fldr)
prices_paid_url = 'http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2018.csv'
prices_paid_fn = os.path.join(data_fldr, 'pp-2018.csv')
geocode_url = 'http://download.geonames.org/export/zip/GB_full.csv.zip'
geocode_zip_fn = os.path.join(data_fldr, 'GB-full.csv.zip')
geocode_fn = os.path.join(data_fldr, 'GB_full.txt')
housing_fn = os.path.join(data_fldr, 'housing.npy')

#get raw data and preprocess if necessary
if not os.path.exists(housing_fn):
  #if prices paid data doesn't exist, download it
  if not os.path.exists(prices_paid_fn):
    print("Prices paid data doesn't exist, downloading")
    download_file(prices_paid_url, prices_paid_fn)
  
  #if geocoding data doesn't exist, download it and unzip the txt
  if not os.path.exists(geocode_fn):
    if not os.path.exists(geocode_zip_fn):
      print("Geocoding data doesn't exist, downloading")
      download_file(geocode_url, geocode_zip_fn)
    print("Unzipping")
    with zipfile.ZipFile(geocode_zip_fn, 'r') as zipf:
      zipf.extractall()
    print("Deleting zip")
    os.remove(geocode_zip_fn)

  print('Loading full GB postcodes database, extracting lat/lon/postcode, converting to dict')
  geodata_fields = ['country code', 'postal_code', 'place_name',
                 'state_name', 'state_code', 'county_name', 'county_code',
                 'community_name', 'community_code',
                 'latitude', 'longitude', 'accuracy']
  geodata = pd.read_csv(geocode_fn, sep='\t', header=0, names=geodata_fields, dtype={'postal_code': str})
  geodata = geodata[['postal_code', 'latitude', 'longitude']]
  geodata = geodata.set_index('postal_code').to_dict('index')
  
  print('Loading price-paid data')
  with open(prices_paid_fn, 'r') as f:
    lines = f.readlines()
  
  
  print('Creating prices paid data using geocode map')
  data = np.zeros((len(lines), 3))
  for i in range(data.shape[0]):
    sys.stdout.write('processing entry ' + str(i+1)+'/'+str(data.shape[0]) + '                            \r')
    sys.stdout.flush()
    tokens = [s.strip(' "') for s in lines[i].split(',')]
    data[i, 2] = int(tokens[1]) #price
    try:
      latlon = geodata[tokens[3]]
      data[i, 0] = latlon['latitude']
      data[i, 1] = latlon['longitude']
    except:
      data[i, 2] = -1 #signal that this is a bad entry
  sys.stdout.write('\n')
  sys.stdout.flush()
  print('Found ' + str(data.shape[0]) + ' entries total, '+str( (data[:, 2] < 0).sum() ) + ' bad entries removed') 
  data = data[data[:, 2] >= 0, :]
  np.save('housing.npy', data)



