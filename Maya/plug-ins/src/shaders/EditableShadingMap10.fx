//////// tweakables
float3 NormalMap;

float ShadeThreshold
<
    string UIName = "Shade Threshold";
    string UIWidget = "Slider";
    float UIMin = 0.000;
    float UIMax = 1.000;
    float UIStep = 0.001;
> = 0.5f;

float DiffuseSmoothness
<
    string UIName = "Diffuse Smoothness";
    string UIWidget = "Slider";
    float UIMin = 0.000;
    float UIMax = 1.000;
    float UIStep = 0.001;
> = 0.4f;

// /// Samplers
// SamplerState TextureSampler
// {

//     Filter = COMPARISON_MIN_MAG_LINEAR_MIP_POINT;
// 	AddressU = Wrap;
// 	AddressV = Wrap;
//     ComparisonFunc = LESS;
// };

// SamplerState SamplerShadowDepth
// {
// 	Filter = MIN_MAG_MIP_POINT;
// 	AddressU = Border;
// 	AddressV = Border;
// 	BorderColor = float4(1.0f, 1.0f, 1.0f, 1.0f);
// };

/// light
float4 lightDir : DIRECTION
<
    string UIName = "Light 0";
	string Object = "Light0_Directional";
	string Space = "World";
> = { 100.0f, 100.0f, 100.0f, 0.0f };

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

#define SHADOW_FILTER_TAPS_CNT 10
float2 SuperFilterTaps[SHADOW_FILTER_TAPS_CNT] 
< 
	string UIWidget = "None"; 
> = 
{ 
    {-0.84052f, -0.073954f}, 
    {-0.326235f, -0.40583f}, 
    {-0.698464f, 0.457259f}, 
    {-0.203356f, 0.6205847f}, 
    {0.96345f, -0.194353f}, 
    {0.473434f, -0.480026f}, 
    {0.519454f, 0.767034f}, 
    {0.185461f, -0.8945231f}, 
    {0.507351f, 0.064963f}, 
    {-0.321932f, 0.5954349f} 
};

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


//////// auto-tracked tweakables
// transform object vertices to world-space:
float4x4 gWorldXf : World < string UIWidget="None"; >;
// transform object normals, tangents, & binormals to world-space:
float4x4 gWorldITXf : WorldInverseTranspose < string UIWidget="None"; >;
// transform object vertices to view space and project them in perspective:
float4x4 gWvpXf : WorldViewProjection < string UIWidget="None"; >;
// provide tranform from "view" or "eye" coords back to world-space:
float4x4 gViewIXf : ViewInverse < string UIWidget="None"; >;


// input from application
struct app2vertex
{
    float4 position : POSITION;
    float2 texCoord : TEXCOORD0;
    float4 normal : NORMAL;
    float4 binormal : BINORMAL0;
    float4 tangent : TANGENT0;
};

// output to pixel shader
struct vertex2pixel
{
    float4 position : POSITION;
    float2 texCoord : TEXCOORD0;
    float3 worldNormal : TEXCOORD1;
    float3 worldBinormal : TEXCOORD2;
    float3 worldTangent : TEXCOORD3;
    float3 worldPosition : TEXCOORD4;
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
vertex2pixel VS_ShadingMap(app2vertex IN)
{
    vertex2pixel Out = (vertex2pixel)0;
    Out.position = mul(IN.position, gWvpXf);
    Out.worldPosition = mul(IN.position, gWorldXf);
    Out.worldNormal = mul(IN.normal, gWorldITXf);
    Out.worldBinormal = mul(IN.binormal, gWorldITXf);
    Out.worldTangent = mul(IN.tangent, gWorldITXf);
    Out.texCoord = float2(IN.texCoord.x, 1.0-IN.texCoord.y);
    return Out; 
}

/*********************************/
/********PIXEL SHADER**********/
/*********************************/
float4 PS_2ShadingMap(vertex2pixel IN) : SV_TARGET
{
    float3 N = (NormalMap.z * IN.worldNormal) + (NormalMap.y * IN.worldBinormal) + (NormalMap.x * IN.worldTangent);
    N = normalize(N);
    float3 L = normalize(lightDir.xyz);
    float diffuse = dot(N, L);
    // float shadow = lightShadow(lightMatrix, lightShadowMap, IN.worldPosition);
    float diffuseSmooth = pow(DiffuseSmoothness, 5);
    float smoothedDiffuse = smoothstep(ShadeThreshold-diffuseSmooth, ShadeThreshold+diffuseSmooth, diffuse);
    float result = lerp(0.0f, 1.0f, smoothedDiffuse/**shadow*/);
    return float4(result, 0.0f, 0.0f, 1.0f);
}


technique10 TwoTones
{
    pass p0
    {
        SetVertexShader(CompileShader(vs_4_0, VS_ShadingMap()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_2ShadingMap()));
    }
}
