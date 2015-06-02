import mpre.base


class Shape(mpre.base.Base):
    
    coordinates = ('x', 'y', 'w', 'h', 'z')  
    colors = ('r', 'g', 'b')
      
    defaults = mpre.base.Base.defaults.copy()
       
    def __init__(self, **kwargs):
        for coordinate in self.coordinates:
            setattr(self, "_" + coordinate, 0)
        super(Shape, self).__init__(**kwargs)
  
    def _on_set(self, coordinate, value):
        setattr(self, "_" + coordinate, value)
        
    def _get_x(self):
        return self._x
    def _set_x(self, value):
        self._on_set('x', value)
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        return self._y
    def _set_y(self, value):
        self._on_set('y', value)
    y = property(_get_y, _set_y)
    
    def _get_position(self):
        return (self.x, self.y)
    def _set_position(self, position):
        self.x, self.y = position
    position = property(_get_position, _set_position)

    def _get_w(self):
        return self._w
    def _set_w(self, value):
        self._on_set('w', value)
    w = property(_get_w, _set_w)
    
    def _get_h(self):
        return self._h
    def _set_h(self, value):
        self._on_set('h', value)
    h = property(_get_h, _set_h)
    
    def _get_z(self):
        return self._z
    def _set_z(self, value):
        self._on_set('z', value)
    z = property(_get_z, _set_z)
    
    def _get_size(self):
        return (self.w, self.h)
    def _set_size(self, size):
        self.w, self.h = size
    size = property(_get_size, _set_size)
    
    def _get_area(self):
        return (self.x, self.y, self.w, self.h)
    def _set_area(self, rect):
        self.x, self.y, self.w, self.h = rect
    area = property(_get_area, _set_area)    
            
    def _get_r(self):
        return self._r
    def _set_r(self, value):
        self._on_set('r', value)
    r = property(_get_r, _set_r)
    
    def _get_g(self):
        return self._g
    def _set_g(self, value):
        self._on_set('g', value)
    g = property(_get_g, _set_g)
    
    def _get_b(self):
        return self._b
    def _set_b(self, value):
        self._on_set('b', value)
    b = property(_get_b, _set_b)
       
    def _get_color(self):
        return (self.r, self.g, self.b)
    def _set_color(self, colors):
        self.r = colors[0]
        self.g = colors[1]
        self.b = colors[2]
    color = property(_get_color, _set_color)  
    
    
class Bounded_Shape(Shape):
       
    defaults = Shape.defaults.copy()
    
    def __init__(self, **kwargs):       
        max_width, max_height = mpre.gui.SCREEN_SIZE
        self.w_range = (0, max_width)
        self.h_range = (0, max_height)
        for color in self.colors:
            setattr(self, color + "_range", (0, 255))
        super(Bounded_Shape, self).__init__(**kwargs)
    
    def _on_set(self, coordinate, value):
        lower_bound, upper_bound = getattr(self, 
                                           coordinate + "_range", (value, value))
        super(Bounded_Shape, self)._on_set(coordinate, 
                                           max(lower_bound, min(value, upper_bound)))
                                           
                                
class Coordinate_Linked(Bounded_Shape):
    
    linked_coordinates = ('x', 'y')
    
    def __init__(self, **kwargs):
        self.linked_shapes = []            
        super(Coordinate_Linked, self).__init__(**kwargs)
            
    def _on_set(self, coordinate, value):
        if coordinate in self.linked_coordinates: 
            for shape in self.linked_shapes:
                setattr(shape, coordinate, value)
        super(Coordinate_Linked, self)._on_set(coordinate, value)