import numpy
import random
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm
from obj import *

pygame.init()

screen = pygame.display.set_mode(
    (800, 800),
    pygame.OPENGL | pygame.DOUBLEBUF
)
model = Obj('./Lab4/face.obj')


vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;
uniform mat4 amatrix;

out vec3 ourColor;
out vec2 fragCoord;

void main()
{
    gl_Position = amatrix * vec4(position, 1.0f);
    ourColor = vertexColor;
    fragCoord = gl_Position.xy;

}
"""

fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;
uniform vec3 color;
in vec3 ourColor;

void main()
{
    // fragColor = vec4(ourColor, 1.0f);
    fragColor = vec4(color, 1.0f);
}
"""
fragment_shader3 = """

#version 460
layout (location = 0) out vec4 fragColor;
in vec3 ourColor;
in vec2 fragCoord;

uniform float iTime;
float colormap_red(float x) {
    if (x < 0.0) {
        return 54.0 / 255.0;
    } else if (x < 20049.0 / 82979.0) {
        return (829.79 * x + 54.51) / 255.0;
    } else {
        return 1.0;
    }
}

float colormap_green(float x) {
    if (x < 20049.0 / 82979.0) {
        return 0.0;
    } else if (x < 327013.0 / 810990.0) {
        return (8546482679670.0 / 10875673217.0 * x - 2064961390770.0 / 10875673217.0) / 255.0;
    } else if (x <= 1.0) {
        return (103806720.0 / 483977.0 * x + 19607415.0 / 483977.0) / 255.0;
    } else {
        return 1.0;
    }
}

float colormap_blue(float x) {
    if (x < 0.0) {
        return 54.0 / 255.0;
    } else if (x < 7249.0 / 82979.0) {
        return (829.79 * x + 54.51) / 255.0;
    } else if (x < 20049.0 / 82979.0) {
        return 127.0 / 255.0;
    } else if (x < 327013.0 / 810990.0) {
        return (792.02249341361393720147485376583 * x - 64.364790735602331034989206222672) / 255.0;
    } else {
        return 1.0;
    }
}

vec4 colormap(float x) {
    return vec4(colormap_red(x), colormap_green(x), colormap_blue(x), 1.0);
}


float rand(vec2 n) { 
    return fract(sin(dot(n, vec2(12.9898, 4.1414))) * 43758.5453);
}

float noise(vec2 p){
    vec2 ip = floor(p);
    vec2 u = fract(p);
    u = u*u*(3.0-2.0*u);

    float res = mix(
        mix(rand(ip),rand(ip+vec2(1.0,0.0)),u.x),
        mix(rand(ip+vec2(0.0,1.0)),rand(ip+vec2(1.0,1.0)),u.x),u.y);
    return res*res;
}

const mat2 mtx = mat2( 0.80,  0.60, -0.60,  0.80 );

float fbm( vec2 p )
{
    float f = 0.0;

    f += 0.500000*noise( p + iTime  ); p = mtx*p*2.02;
    f += 0.031250*noise( p ); p = mtx*p*2.01;
    f += 0.250000*noise( p ); p = mtx*p*2.03;
    f += 0.125000*noise( p ); p = mtx*p*2.01;
    f += 0.062500*noise( p ); p = mtx*p*2.04;
    f += 0.015625*noise( p + sin(iTime) );

    return f/0.96875;
}

float pattern( in vec2 p )
{
	return fbm( p + fbm( p + fbm( p ) ) );
}

void main( )
{
    vec2 iResolution = vec2(0.5, 0.5);
    vec2 uv = fragCoord/iResolution.x;
	float shade = pattern(uv);
    fragColor = vec4(colormap(shade).rgb, shade);
}
"""
fragment_shader4 = '''
#version 460
layout (location = 0) out vec4 fragColor;
in vec3 ourColor;
in vec2 fragCoord;
uniform float iTime;
float map(vec3 p) {
	vec3 n = vec3(0, 1, 0);
	float k1 = 1.9;
	float k2 = (sin(p.x * k1) + sin(p.z * k1)) * 0.8;
	float k3 = (sin(p.y * k1) + sin(p.z * k1)) * 0.8;
	float w1 = 4.0 - dot(abs(p), normalize(n)) + k2;
	float w2 = 4.0 - dot(abs(p), normalize(n.yzx)) + k3;
	float s1 = length(mod(p.xy + vec2(sin((p.z + p.x) * 2.0) * 0.3, cos((p.z + p.x) * 1.0) * 0.5), 2.0) - 1.0) - 0.2;
	float s2 = length(mod(0.5+p.yz + vec2(sin((p.z + p.x) * 2.0) * 0.3, cos((p.z + p.x) * 1.0) * 0.3), 2.0) - 1.0) - 0.2;
	return min(w1, min(w2, min(s1, s2)));
}

vec2 rot(vec2 p, float a) {
	return vec2(
		p.x * cos(a) - p.y * sin(a),
		p.x * sin(a) + p.y * cos(a));
}

void main() {
    float time = iTime;
    vec2 iResolution = vec2(0.5,0.5);
	vec2 uv = ( fragCoord.xy / iResolution.xy ) * 2.0 - 1.0;
	uv.x *= iResolution.x /  iResolution.y;
	vec3 dir = normalize(vec3(uv, 1.0));
	dir.xz = rot(dir.xz, time * 0.23);dir = dir.yzx;
	dir.xz = rot(dir.xz, time * 0.2);dir = dir.yzx;
	vec3 pos = vec3(0, 0, time);
	vec3 col = vec3(0.0);
	float t = 0.0;
    float tt = 0.0;
	for(int i = 0 ; i < 100; i++) {
		tt = map(pos + dir * t);
		if(tt < 0.001) break;
		t += tt * 0.45;
	}
	vec3 ip = pos + dir * t;
	col = vec3(t * 0.1);
	col = sqrt(col);
	fragColor = vec4(0.05*t+abs(dir) * col + max(0.0, map(ip - 0.1) - tt), 1.0); //Thanks! Shane!
    fragColor.a = 1.0 / (t * t * t * t);
}

'''
fragment_shader5 = '''
#version 460
layout (location = 0) out vec4 fragColor;
in vec3 ourColor;
in vec2 fragCoord;
uniform float iTime;
float opSmoothUnion( float d1, float d2, float k )
{
    float h = clamp( 0.876 + 1.284*(d2-d1)/k, 0.112, 2.616 );
    return mix( d2, d1, h ) - k*h*(1.0-h);
}

float sdSphere( vec3 p, float s )
{
  return length(p)-s;
} 

float map(vec3 p)
{
	float d = 0.480;
	for (int i = 0; i < 16; i++)
	{
		float fi = float(i);
		float time = iTime * (fract(fi * 412.531 + 1.073) - 1.020) * 1.152;
		d = opSmoothUnion(
            sdSphere(p + sin(time + fi * vec3(52.5126, 64.62744, 632.25)) * vec3(2.0, 2.0, 0.8), mix(0.5, 1.0, fract(fi * 412.531 + 0.5124))),
			d,
			0.024
		);
	}
	return d;
}

vec3 calcNormal( in vec3 p )
{
    const float h = 1e-5; // or some other value
    const vec2 k = vec2(1,-1);
    return normalize( k.xyy*map( p + k.xyy*h ) + 
                      k.yyx*map( p + k.yyx*h ) + 
                      k.yxy*map( p + k.yxy*h ) + 
                      k.xxx*map( p + k.xxx*h ) );
}

void main()
{
    vec2 iResolution = vec2(0.5, 0.5);
    vec2 uv = fragCoord/iResolution.xy;
    
    // screen size is 6m x 6m
	vec3 rayOri = vec3((uv - 0.5) * vec2(iResolution.x/iResolution.y, 0.368) * 6.0, 3.0);
	vec3 rayDir = vec3(0.0, 0.0, -1.0);
	
	float depth = 0.0;
	vec3 p;
	
	for(int i = 0; i < 64; i++) {
		p = rayOri + rayDir * depth;
		float dist = map(p);
        depth += dist;
		if (dist < 1e-6) {
			break;
		}
	}
	
    depth = min(6.0, depth);
	vec3 n = calcNormal(p);
    float b = max(0.0, dot(n, vec3(0.577)));
    vec3 col = (0.5 + 0.5 * cos((b + iTime * 3.0) + uv.xyx * 2.0 + vec3(0,2,4))) * (0.85 + b * 0.35);
    col *= exp( -depth * 0.15 );
	
    // maximum thickness is 2m in alpha channel
    fragColor = vec4(col, 0.0 );
}
'''

#Agregar shaders en shadertoy
#Variables fragcord , time , resolution 
#Definir resolucion 
compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)

compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
compiled_fragment_shader2 = compileShader(fragment_shader3, GL_FRAGMENT_SHADER)
compiled_fragment_shader3 = compileShader(fragment_shader4, GL_FRAGMENT_SHADER)
compiled_fragment_shader4 = compileShader(fragment_shader5, GL_FRAGMENT_SHADER)

shader = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader
)
shader2 = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader2
)
shader3 = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader3
)
shader4 = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader4
)

glUseProgram(shader)

vertex = []
tvertices = len(model.vertices)
tfaces = len(model.faces)

for i in range(tvertices):
    for j in range(len(model.vertices[i])):
        vertex.append(model.vertices[i][j])
faces = []
for i in range(tfaces):
    for j in range(len(model.faces[i])):
        faces.append(int(model.faces[i][j][0]-1))

        

vertex_data = numpy.array(vertex, dtype=numpy.float32)
vertex_array_object = glGenVertexArrays(1)

faces_data = numpy.array(faces, dtype=numpy.int32)

glBindVertexArray(vertex_array_object)

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(
    GL_ARRAY_BUFFER,  # tipo de datos
    vertex_data.nbytes,  # tamaño de da data en bytes    
    vertex_data, # puntero a la data
    GL_STATIC_DRAW
)

glVertexAttribPointer(
    0,
    3,
    GL_FLOAT,
    GL_FALSE,
    3 * 4,
    ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)


element_buffer_object = glGenBuffers(1)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces_data.nbytes, faces_data, GL_STATIC_DRAW)



def calculateMatrix(angle,mov,zoom):
    i = glm.mat4(1)
    translate = glm.translate(i, glm.vec3(0, 0, 0))

    rotate = glm.rotate(i, glm.radians(angle), glm.vec3(0, 1, 0))

    scale = glm.scale(i, glm.vec3(1, 1, 1))

    model = translate * rotate * scale

    view = glm.lookAt(
        glm.vec3(0, mov, zoom),
        glm.vec3(0, 0, 0),
        glm.vec3(0, 2, 0)
    )

    projection = glm.perspective(
        glm.radians(45),
        1600/1200,
        0.1,
        1000.0
    )

    amatrix = projection * view * model

    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'amatrix'),
        1,
        GL_FALSE,
        glm.value_ptr(amatrix)
    )


glViewport(0, 0, 800, 800)



running = True

glClearColor(0.14, 0.16, 0.31, 1)

r = 0
mov = 0
zoom = 5
prev_iTime = pygame.time.get_ticks()
activeShader = shader
rotar = False
while running:
    glClear(GL_COLOR_BUFFER_BIT)

    color1 = random.random()
    color2 = random.random()
    color3 = random.random()

    color = glm.vec3(color1, color2, color3)

    glUniform3fv(
        glGetUniformLocation(activeShader,'color'),
        1,
        glm.value_ptr(color)
    )
    iTime = (pygame.time.get_ticks() - prev_iTime) / 1000
    glUniform1f(
        glGetUniformLocation(activeShader, "iTime"),
        iTime
    )


    calculateMatrix(r,mov,zoom)

    pygame.time.wait(50)


    glDrawElements(GL_TRIANGLES, len(faces_data),GL_UNSIGNED_INT, None)

    
    r += 5
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mov += 5
            if event.key == pygame.K_DOWN:
                mov -= 5
            #Cambiar al primer shader
            if event.key == pygame.K_a:
                glUseProgram(shader2)
                activeShader = shader2
            if event.key == pygame.K_s:
                glUseProgram(shader3)
                activeShader = shader3
            if event.key == pygame.K_d:
                glUseProgram(shader4)
                activeShader = shader4

        if event.type == pygame.MOUSEWHEEL:
            zoom -= event.y
        
        if event.type == pygame.QUIT:
            running = False