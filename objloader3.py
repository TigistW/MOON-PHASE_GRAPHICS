from re import I
import numpy as np
class model_object_loader:
    buffer = []
    @staticmethod
    def vertice_allocation(indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: 
                start = ind * 3
                end = start + 3
                model_object_loader.buffer.extend(vertices[start:end])
            elif i % 3 == 1: 
                start = ind * 2
                end = start + 2
                model_object_loader.buffer.extend(textures[start:end])
            elif i % 3 == 2: 
                start = ind * 3
                end = start + 3
                model_object_loader.buffer.extend(normals[start:end])

    @staticmethod
    def get_model(file):
        vertex_coordinates = []  
        texture_coordinates = []  
        normal_coordinates = [] 

        vertices = [] 
        indices = []

        with open(file, 'r') as f:
            segment = f.readline()
            while segment:
                data = segment.split()
                if data[0] == 'v':
                    for i in data:
                        if i == 'v':
                            continue
                        vertex_coordinates.append(float(i))
                elif data[0] == 'vt':
                    for i in data:
                        if i == 'vt':
                            continue
                        texture_coordinates.append(float(i))

                elif data[0] == 'vn':
                    for i in data:
                        if i == 'vn':
                            continue
                        normal_coordinates.append(float(i))

                elif data[0] == 'f':
                    for value in data[1:]:
                        val = value.split('/')
                        for i in val:
                            if i == 'f':
                                continue
                            vertices.append(int(i)-1)
                        indices.append(int(val[0])-1)
                segment = f.readline()

        for i,vert in enumerate(vertices):
            if i % 3 == 0:
                begin = vert * 3
                end = begin + 3
                model_object_loader.buffer.extend(vertex_coordinates[begin:end])
            elif i % 3 == 1:
                begin = vert * 2
                end = begin + 2
                model_object_loader.buffer.extend(texture_coordinates[begin:end])
            elif i % 3 == 2:
                begin = vert * 3
                end = begin + 3
                model_object_loader.buffer.extend(normal_coordinates[begin:end])

        buffer = model_object_loader.buffer.copy()
        model_object_loader.buffer = []

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')
