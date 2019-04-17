def create_image():
    test_img = pyglet.image.load('frame.png').get_image_data()
    w = 120
    h = 100
    blank = pyglet.image.Texture.create(600,700)
    blank.blit_into(test_img,w*2,0,0)
    blank.blit_into(test_img,w*2,h*6,0)
    for i in range(1,6,1):
        for i2 in range(5):
            blank.blit_into(test_img,w*i2,h*i,0)
    blank.save('blank.png')

create_image()

"""
        image = pyglet.resource.image('smile.png')                                                                                                                                                               
        texture = image.get_texture()   
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)                                                                                                                               
        texture.width = 120 # resize from 8x8 to 16x16                                                                                                                                                                  
        texture.height = 100                                                                                                                                                                                                                                                                                                                       
        self.tex = texture
        
        self.pos_ti = [0,0]

"""
