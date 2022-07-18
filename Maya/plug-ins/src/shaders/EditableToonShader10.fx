//////// tweakables
Texture2D BaseTexture : Color
<
    string UIName = "Base Color Map";
    int mipmaplevels = 0;
>;

Texture2D ShadingMap
<
	string UIWidget = "None"; 
    int mipmaplevels = 0;
>;

float ShadeIntensityRatio
<
    string UIName = "Shade Intensity Ratio";
    string UIWidget = "Slider";
    float UIMin = 0.000;
    float UIMax = 1.000;
    float UIStep = 0.001;
> = 0.2f;

/// Samplers
SamplerState TextureSampler
{

    Filter = COMPARISON_MIN_MAG_LINEAR_MIP_POINT;
	AddressU = Wrap;
	AddressV = Wrap;
    ComparisonFunc = LESS;
};

SamplerState SamplerShadowDepth
{
	Filter = MIN_MAG_MIP_POINT;
	AddressU = Border;
	AddressV = Border;
	BorderColor = float4(1.0f, 1.0f, 1.0f, 1.0f);
};

/// light
float4 lightColor : LIGHTCOLOR
<
    string UIName = "Light 0 Color";
	string Object = "Light0_Directional";
    string UIWidget = "Color";
> = { 1.0f, 1.0f, 1.0f, 1.0f};

// Texture2D lightShadowMap : SHADOWMAP
// <
// 	string Object = "Light0_Directional";
// 	string UIWidget = "None";
// >;

// float4x4 lightMatrix : SHADOWMAPMATRIX		
// < 
//     string Object = "Light0_Directional";
//     string UIWidget = "None"; 
// >;

// #define SHADOW_FILTER_TAPS_CNT 10
// float2 SuperFilterTaps[SHADOW_FILTER_TAPS_CNT] 
// < 
// 	string UIWidget = "None"; 
// > = 
// { 
//     {-0.84052f, -0.073954f}, 
//     {-0.326235f, -0.40583f}, 
//     {-0.698464f, 0.457259f}, 
//     {-0.203356f, 0.6205847f}, 
//     {0.96345f, -0.194353f}, 
//     {0.473434f, -0.480026f}, 
//     {0.519454f, 0.767034f}, 
//     {0.185461f, -0.8945231f}, 
//     {0.507351f, 0.064963f}, 
//     {-0.321932f, 0.5954349f} 
// };

// float shadowMapTexelSize 
// < 
// 	string UIWidget = "None"; 
// > = {0.00195313}; // (1.0f / 512)

// float shadowDepthBias : ShadowMapBias
// <
//     string UIGroup = "Lighting";
//     string UIWidget = "Slider";
//     float UIMin = 0.000;
//     float UISoftMax = 0.1;
//     float UIStep = 0.001;
//     string UIName = "Shadow Bias";
// > = {0.01f};

bool LinearSpaceLighting
<
    string UIGroup = "Lighting";
    string UIName = "Linear Space Lighting";
    int UIOrder = 10;
> = true;

//////// auto-tracked tweakables
// transform object vertices to world-space:
float4x4 gWorldXf : World < string UIWidget="None"; >;
// transform object normals, tangents, & binormals to world-space:
float4x4 gWorldITXf : WorldInverseTranspose < string UIWidget="None"; >;
// transform object vertices to view space and project them in perspective:
float4x4 gWvpXf : WorldViewProjection < string UIWidget="None"; >;
// provide tranform from "view" or "eye" coords back to world-space:
float4x4 gViewIXf : ViewInverse < string UIWidget="None"; >;

bool MayaFullScreenGamma : MayaGammaCorrection < string UIWidget = "None"; >;

// input from application
struct app2vertex
{
    float4 position : POSITION;
    float2 texCoord : TEXCOORD0;
};

// output to pixel shader
struct vertex2pixel
{
    float4 position : POSITION;
    float2 texCoord : TEXCOORD0;
};

// float lightShadow(float4x4 LightViewPrj, uniform Texture2D ShadowMapTexture, float3 VertexWorldPosition)
// {	
// 	float shadow = 1.0f;

// 	float4 Pndc = mul( float4(VertexWorldPosition.xyz,1.0) ,  LightViewPrj); 
// 	Pndc.xyz /= Pndc.w; 
// 	if ( Pndc.x > -1.0f && Pndc.x < 1.0f && Pndc.y  > -1.0f   
// 		&& Pndc.y <  1.0f && Pndc.z >  0.0f && Pndc.z <  1.0f ) 
// 	{ 
// 		float2 uv = 0.5f * Pndc.xy + 0.5f; 
// 		uv = float2(uv.x,(1.0-uv.y));	// maya flip Y
// 		float z = Pndc.z - shadowDepthBias / Pndc.w; 

// 		// we'll sample a bunch of times to smooth our shadow a little bit around the edges:
// 		shadow = 0.0f;
// 		for(int i=0; i<SHADOW_FILTER_TAPS_CNT; ++i) 
// 		{ 
// 			float2 suv = uv + (SuperFilterTaps[i] * shadowMapTexelSize);
// 			float val = z - ShadowMapTexture.SampleLevel(SamplerShadowDepth, suv, 0 ).x;
// 			shadow += (val >= 0.0f) ? 0.0f : (1.0f / SHADOW_FILTER_TAPS_CNT);
// 		}

// 		// a single sample would be:
// 		// shadow = 1.0f;
// 		// float val = z - ShadowMapTexture.SampleLevel(SamplerShadowDepth, uv, 0 ).x;
// 		// shadow = (val >= 0.0f)? 0.0f : 1.0f;
		
// 		// shadow = lerp(1.0f, shadow, shadowMultiplier);  
// 	} 

// 	return shadow;
// }

/*********************************/
/********VERTEX SHADER**********/
/*********************************/
vertex2pixel vertex(app2vertex IN)
{
    vertex2pixel Out = (vertex2pixel)0;
    Out.position = mul(IN.position, gWvpXf);
    Out.texCoord = float2(IN.texCoord.x, 1.0-IN.texCoord.y);
    return Out; 
}

/*********************************/
/********PIXEL SHADER**********/
/*********************************/
float4 pixel2tones(vertex2pixel IN) : COLOR
{
    float4 col = BaseTexture.Sample(TextureSampler, IN.texCoord);
    float diffuse = ShadingMap.Sample(TextureSampler. IN.texCoord);
    col *= lerp(ShadeIntensityRatio, 1.0f, diffuse) * lightColor;

	float gammaCorrection = lerp(1.0, 2.2, LinearSpaceLighting);
    if (!MayaFullScreenGamma)
		col = pow(col, 1/gammaCorrection);
    
    return col;
}


technique10 TwoTones
{
    pass p0
    {
        SetVertexShader(CompileShader(vs_4_0, vertex()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, pixel2tones()));
    }
}
