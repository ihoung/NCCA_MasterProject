from string import *
import textwrap


def getShaderSurfaceFragment(editNum):
    surfaceFragmentBody = textwrap.dedent("""
        <fragment_graph  name=\"ETS_ShaderSurface\" ref=\"ETS_ShaderSurface\" class=\"FragmentGraph\" version=\"1.0\" >
        <description></description>
        <fragments>
            <fragment_ref name=\"ETS_Toon\" ref=\"ETS_ToonFragment\" />
            <fragment_ref name=\"ETS_ShadingMap\" ref=\"ETS_ShadingMapFragment\" />
        </fragments>
        <connections>
            <connect from=\"ETS_ShadingMap.output\" to=\"ETS_Toon.DiffuseShading\" name=\"diffuseShading\" />
        </connections>
        <properties>
            <float3 name=\"baseColor\" ref=\"ETS_Toon.BaseColor\" />"
            <float3 name=\"Nw\" ref=\"ETS_ShadingMap.Nw\" semantic=\"Nw\" flags=\"varyingInputParam\" />
            <float2 name=\"uvCoord\" ref=\"ETS_ShadingMap.uvCoord\" semantic=\"mayaUvCoordSemantic\" flags=\"varyingInputParam\" />
            <float3 name=\"Lw\" ref=\"ETS_ShadingMap.Lw\" />
            <float  name=\"shadeThreshold\" ref=\"ETS_ShadingMap.ShadeThreshold\" />
            <float  name=\"diffuseSmoothness\" ref=\"ETS_ShadingMap.DiffuseSmoothness\" />
            <float3 name=\"diffuseI\" ref=\"ETS_Toon.diffuseI\" />
            <float  name=\"shadeIntensityRatio\" ref=\"ETS_Toon.ShadeIntensityRatio\" /> ^1s
        </properties>
        <values>
            <float3 name=\"baseColor\" value=\"0.500000,0.500000,0.500000\" />
            <float3 name=\"Lw\" value=\"0.000000,0.000000,0.000000\"  />
            <float3 name=\"diffuseI\" value=\"0.000000,0.000000,0.000000\" />
            <float name=\"shadeThreshold\" value=\"0.500000\"  />
            <float name=\"diffuseSmoothness\" value=\"0.400000\"  />
            <float name=\"shadeIntensityRatio\" value=\"0.200000\"  />
        </values>
        <outputs>
            <float3  name=\"outColor\" ref=\"ETS_Toon.outColor\" />
        </outputs>
        </fragment_graph>
    """)
    insertBody = ""
    for i in range(editNum):
        insertBody += "\n<float  name=\"sharpness{}\" ref=\"ETS_Toon.sharpness\" />".format(i)
    surfaceFragmentBody = replace(surfaceFragmentBody, "^1s", insertBody)
    return surfaceFragmentBody