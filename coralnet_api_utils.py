import numpy as np
import json


def get_points(height, width, offset, percentage, sampling_method):
    '''
    height: the height of the image (rows)
    width: the width of the image (columns)
    offset: the % of pixels on all sides to avoid sampling (i.e. avoids edges of image)
    percentage: the % of points to sample (1% of a 4MP image = 40,000 points)
    sampling_method: either "random" or "grid"
    '''

    percentage = percentage * .01

    h_offset = int(offset * .01 * height)
    w_offset = int(offset * .01 * width)

    num_points = int(height * width * percentage)

    if(sampling_method == 'random'):

        x = np.random.randint(w_offset, width - w_offset, num_points)
        y = np.random.randint(h_offset, height - h_offset, num_points)
        
    else:
        
        density = int(np.sqrt(num_points)) 

        # Creates an equally spaced grid, reshapes, converts into list
        x_, y_ = np.meshgrid(np.linspace(w_offset, width - w_offset, density), 
                             np.linspace(h_offset, height - h_offset, density))

        xy = np.dstack([x_, y_]).reshape(-1, 2).astype(int)

        x = [point[0] for point in xy]
        y = [point[1] for point in xy]

        # Any labels that did not fit in the grid will be sampled randomly
        x += np.random.randint(w_offset, width - w_offset, num_points - len(xy)).tolist()
        y += np.random.randint(h_offset, height - h_offset, num_points - len(xy)).tolist()


    points = []

    for _ in range(num_points):
        points.append({'row': int(y[_]), 'column': int(x[_])})
        
    return points


def decode_status(r_status):
    
    curr_status = json.loads(r_status.content) 
    message = ''
    
    if 'status' in curr_status['data'][0]['attributes'].keys(): 
    
        s = curr_status['data'][0]['attributes']['successes'] 
        f = curr_status['data'][0]['attributes']['failures'] 
        t = curr_status['data'][0]['attributes']['total']
        status = curr_status['data'][0]['attributes']['status'] 
        ids = curr_status['data'][0]['id'].split(",")
        ids = ''.join(str(_) for _ in ids)

        message = 'Success: ' + str(s) + ' Failures: ' + str(f) + ' Total: ' + str(t) + ' Status: ' + str(status) + ' Ids: ' + ids
    
    return curr_status, message