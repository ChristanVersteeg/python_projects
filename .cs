using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;

public class MeshGeneration : MonoBehaviour
{
    [SerializeField] private Material material;

    Vector3[] verts = new Vector3[7];

    int[] tris = new int[18];

    private Mesh mesh;
    private GameObject meshObject;


    [SerializeField] private Vector3Int pain;


    private void SetMesh()
    {
        verts[0] = new Vector3(0, 1);
        verts[1] = new Vector3(1, 1);
        verts[2] = new Vector3(0, 0);
        verts[3] = new Vector3(1, 0);

        verts[4] = new Vector3(0, 1, 1);
        verts[5] = new Vector3(1, 1, 1);

        verts[6] = new Vector3(0, 0, 1);

        tris[0] = 0;
        tris[1] = 1;
        tris[2] = 2;

        tris[3] = 2;
        tris[4] = 1;
        tris[5] = 3;


        tris[6] = 0;
        tris[7] = 4;
        tris[8] = 5;

        tris[9] = 0;
        tris[10] = 5;
        tris[11] = 1;


        tris[12] = 2;
        tris[13] = 6;
        tris[14] = 0;

        tris[15] = 4;
        tris[16] = 0;
        tris[17] = 6;
    }

    private void CreateMesh()
    {
        mesh = new();

        mesh.vertices = verts;
        mesh.triangles = tris;

        meshObject = new GameObject(nameof(meshObject));
        meshObject.AddComponent<MeshFilter>().mesh = mesh;
        meshObject.AddComponent<MeshRenderer>().material = material;
    }

    void Start()
    {
        SetMesh();
        CreateMesh();
    }

    Color debugColor = new(0.310f, 0.620f, 0.275f, 0.75f);

    private void OnDrawGizmos()
    {
        if (mesh == null) return;

        Gizmos.color = debugColor;

        for (int i = 0; i < mesh.vertices.Length; i++)
            Gizmos.DrawSphere(mesh.vertices[i], .025f);
    }
}
