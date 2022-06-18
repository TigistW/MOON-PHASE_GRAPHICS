# version 330
in vec2 v_texture;
in vec3 fragNormal;
out vec4 out_color;
uniform sampler2D s_texture;
void main()
{   
    vec3 ambientIntensity = vec3(0.25f, 0.25f, 0.25f);
    vec3 sunIntensity = vec3(1.0,1.0,1.0);
    vec3 sunDirection = normalize(vec3(-05.0f,02.0f, 03.0f));

    vec4 element = texture(s_texture, v_texture);
    vec3 lightIntensity = ambientIntensity + sunIntensity * max(dot(fragNormal, sunDirection), 0.0f);
    out_color = vec4(element.rgb * lightIntensity, element.a);
}