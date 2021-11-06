from geopy.distance import distance

def getNearestObject(long, lat, datasets):
    nearestObject = datasets[0]
    minDistance = 99999999
    for dataset in datasets:
        dataSetPosition = (dataset.long, dataset.lat)
        referencePosition = (long, lat)
        dataset.distanceInKm = round(distance(dataSetPosition, referencePosition).km, 2)
        if(dataset.distanceInKm < minDistance):
            minDistance = dataset.distanceInKm
            nearestObject = dataset
            
    return nearestObject