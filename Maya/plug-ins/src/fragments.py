from string import *
import textwrap


def getShaderSurfaceFragment(editNum):
    # surfaceFragmentBody = textwrap.dedent("""
    #     <fragment_graph  name=\"ETS_ShaderSurface\" ref=\"ETS_ShaderSurface\" class=\"FragmentGraph\" version=\"1.0\" >
    #     <description></description>
    #     <fragments>
    #         <fragment_ref name=\"ETS_Toon\" ref=\"ETS_ToonFragment\" />
    #         <fragment_ref name=\"ETS_ShadingMap\" ref=\"ETS_ShadingMapFragment\" />
    #     </fragments>
    #     <connections>
    #         <connect from=\"ETS_ShadingMap.output\" to=\"ETS_Toon.DiffuseShading\" name=\"diffuseShading\" />
    #     </connections>
    #     <properties>
    #         <float3 name=\"baseColor\" ref=\"ETS_Toon.BaseColor\" />"
    #         <float3 name=\"Nw\" ref=\"ETS_ShadingMap.Nw\" semantic=\"Nw\" flags=\"varyingInputParam\" />
    #         <float2 name=\"uvCoord\" ref=\"ETS_ShadingMap.uvCoord\" semantic=\"mayaUvCoordSemantic\" flags=\"varyingInputParam\" />
    #         <float3 name=\"Lw\" ref=\"ETS_ShadingMap.Lw\" />
    #         <float  name=\"shadeThreshold\" ref=\"ETS_ShadingMap.ShadeThreshold\" />
    #         <float  name=\"diffuseSmoothness\" ref=\"ETS_ShadingMap.DiffuseSmoothness\" />
    #         <float3 name=\"diffuseI\" ref=\"ETS_Toon.diffuseI\" />
    #         <float  name=\"shadeIntensityRatio\" ref=\"ETS_Toon.ShadeIntensityRatio\" /> ^1s
    #     </properties>
    #     <values>
    #         <float3 name=\"baseColor\" value=\"0.500000,0.500000,0.500000\" />
    #         <float3 name=\"Lw\" value=\"0.000000,0.000000,0.000000\"  />
    #         <float3 name=\"diffuseI\" value=\"0.000000,0.000000,0.000000\" />
    #         <float name=\"shadeThreshold\" value=\"0.500000\"  />
    #         <float name=\"diffuseSmoothness\" value=\"0.400000\"  />
    #         <float name=\"shadeIntensityRatio\" value=\"0.200000\"  />
    #     </values>
    #     <outputs>
    #         <float3  name=\"outColor\" ref=\"ETS_Toon.outColor\" />
    #     </outputs>
    #     </fragment_graph>
    # """)
    surfaceFragmentBody = textwrap.dedent("""
    <fragment  uiName="ETS_ToonFragment" name="ETS_ToonFragment" type="plumbing" class="ShadeFragment" version="1.0" feature_level="30" >
    <description>
<![CDATA[
Toon renderer. Uses pre-processed shade map to render the final shading color.]]>
    </description>
    <properties>
        <float3  name="baseColor" /> ^1s
    </properties>
    <values>
        <float3 name="baseColor" value="0.5,0.5,0.5" /> ^2s
    </values>
    <outputs>
        <float3  name="outColor" />
    </outputs>
    <parametershare>
    </parametershare>
    <implementation >
    <implementation render="OGSRenderer" language="Cg" lang_version="2.100000" >
        <function_name val="ETSToonFragment" />
        <source>
            <![CDATA[
    float3 ETSToonFragment(
        float3 baseColor ^3s
    )
    {
        float3 col = baseColor; ^4s
        return col;
    }
                ]]>
            </source>
        </implementation>
        <implementation render="OGSRenderer" language="HLSL" lang_version="11.000000" >
            <function_name val="ETSToonFragment" />
            <source>
                <![CDATA[
    float3 ETSToonFragment(
        float3 baseColor ^3s
    )
    {
        float3 col = baseColor; ^4s
        return col;
    }
                ]]>
            </source>
        </implementation>
        <implementation render="OGSRenderer" language="GLSL" lang_version="3.000000" >
            <function_name val="ETSToonFragment" />
            <source>
                <![CDATA[
    vec3 ETSToonFragment(
        vec3 baseColor ^3s
    )
    {
        vec3 col = baseColor; ^4s
        return col;
    }
                ]]>
            </source>
        </implementation>
        </implementation>
    </fragment>
    """)
    insertBody_1 = ""
    insertBody_2 = ""
    insertBody_3 = ""
    insertBody_4 = ""
    for i in range(editNum):
        insertBody_1 += "\n<float  name=\"sharpness_{}\" />".format(i)
        insertBody_2 += "\n<float name=\"sharpness_{}\" value=\"0.0f\">".format(i)
        insertBody_3 += ", float sharpness_{}".format(i)
        insertBody_4 += "\ncol *= sharpness_{};".format(i)
    surfaceFragmentBody = replace(surfaceFragmentBody, "^1s", insertBody_1)
    surfaceFragmentBody = replace(surfaceFragmentBody, "^2s", insertBody_2)
    surfaceFragmentBody = replace(surfaceFragmentBody, "^3s", insertBody_3)
    surfaceFragmentBody = replace(surfaceFragmentBody, "^4s", insertBody_4)
    return surfaceFragmentBody