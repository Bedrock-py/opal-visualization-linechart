#****************************************************************
#
# Copyright (c) 2015, Georgia Tech Research Institute
# All rights reserved.
#
# This unpublished material is the property of the Georgia Tech
# Research Institute and is protected under copyright law.
# The methods and techniques described herein are considered
# trade secrets and/or confidential. Reproduction or distribution,
# in whole or in part, is forbidden except by the express written
# permission of the Georgia Tech Research Institute.
#****************************************************************/

from bedrock.visualization.utils import *
import vincent, json


def get_classname():
    return 'Linechart'
    
class Linechart(Visualization):
    def __init__(self):
        super(Linechart, self).__init__()
        self.inputs = ['matrix.csv', 'features.txt', 'selected_features']
        self.parameters = ['matrix','features', 'selected_features']
        self.parameters_spec = []
        self.name = 'Linechart'
        self.description = ''

    def initialize(self, inputs):
        self.features = load_features(inputs['features.txt']['rootdir'] + 'features.txt')
        self.matrix = load_dense_matrix(inputs['matrix.csv']['rootdir'] + 'matrix.csv', names=self.features)
        self.selected_features = inputs['selected_features']

    def create(self):
        lines = vincent.Line(self.matrix[self.selected_features], iter_idx=self.selected_features[0])
        lines.legend(title='Categories')
        json_content = lines.to_json()
        data = json.loads(json_content)
        dateAxis = False
        for idx, scale in enumerate(data['scales']):
            if scale['name'] == 'x':
                if dateAxis is True:
                    data['scales'][idx]['type'] = 'time'
                else:
                    data['scales'][idx]['zero'] = False

        json_content = json.dumps(data)

        vis_id = 'vis_' + get_new_id()
        script = '<script> spec =' + json_content + ';vg.parse.spec(spec, function(chart) { chart({el:"#' + vis_id + '"}).update(); });</script>'
        
        return {'data':script,'type':'default', 'id': vis_id, 'title': 'Linechart'}
