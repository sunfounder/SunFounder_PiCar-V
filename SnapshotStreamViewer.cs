
using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class SnapshotStreamViewer : MonoBehaviour
{
    public string snapshotUrl = "http://10.0.0.8:8080/?action=snapshot";
    public Renderer targetRenderer;
    public float interval = 1f / 50f; // Fetch 10 snapshots per second (10 FPS)
    public float retryDelay = 5f; // Retry after 5 seconds if there's an error

    private void Start()
    {
        if (targetRenderer == null)
        {
            targetRenderer = GetComponent<Renderer>();
        }

        if (targetRenderer != null)
        {
            StartCoroutine(GetSnapshotStream());
        }
    }

    private IEnumerator GetSnapshotStream()
    {
        while (true)
        {
            bool isError = false;
            using (UnityWebRequest request = UnityWebRequestTexture.GetTexture(snapshotUrl))
            {   
                try
                {
                    Debug.Log("Sending request to: " + snapshotUrl);
                    yield return request.SendWebRequest();
                    if (request.result == UnityWebRequest.Result.Success)
                    {
                        Texture2D texture = DownloadHandlerTexture.GetContent(request);
                        targetRenderer.material.mainTexture = texture;
                    }
                    else
                    {
                        Debug.LogError("Error while fetching snapshot: " + request.error);
                        isError = true;
                    }
                }
                catch (Exception e)
                {
                    Debug.LogError("Error: " + e.Message);
                    isError = true;
                }
            }

            if (isError)
            {
                yield return new WaitForSeconds(retryDelay);
            }
            else
            {
                yield return new WaitForSeconds(interval);
            }
        }
    }
}
