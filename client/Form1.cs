using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;

using OpenCvSharp;
using OpenCvSharp.Extensions;

using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Net;
using System.IO;

namespace CamSender
{
    public partial class Form1 : Form
    {
        OpenCvSharp.VideoCapture _capture;

        String _email = "test@email.com";

        const String _base_url = "http://localhost:8080/";
        const String _template_url = _base_url + "learn";
        const String _analysis_url = _base_url + "process";

        bool _is_started = false;
        CancellationTokenSource _cts;

        private void ProcessTemplate()
        {
            List<Mat> frames = new List<Mat>();

            for(int i = 0; i < 5; ++i)
            {
                using (var frameMat = _capture.RetrieveMat())
                {

                    var frameBitmap = BitmapConverter.ToBitmap(frameMat);
                    pictureBox1.Image = frameBitmap;
                    frames.Add(frameMat.Clone());
                }

                Thread.Sleep(1000);
            }

            String message = MakeLearnJson(frames);

            SendMessage(_template_url, message);
        }

        private void ProcessAnalysis()
        {
            while (true)
            {
                _cts.Token.ThrowIfCancellationRequested();
                using (var frameMat = _capture.RetrieveMat())
                {
                    var frameBitmap = BitmapConverter.ToBitmap(frameMat);
                    pictureBox1.Image = frameBitmap;

                    SendMessage(_analysis_url, MakeAnalysisJson(frameMat));                
                }

                Thread.Sleep(500);
            }
                        
        }

        static private String PackFrame(Mat frame)
        {
            var bytes = frame.ImEncode(".jpg");
            return Convert.ToBase64String(bytes, 0, bytes.Length);
        }

        private String MakeLearnJson(List<Mat> frames)
        {
            dynamic message = new JObject();
            message.email = _email;
            message.frames = new JArray();
            foreach (var frame in frames)
            {
                message.frames.Add(PackFrame(frame));
            }

            return message.ToString();
        }

        private String MakeAnalysisJson(Mat frame)
        {
            dynamic message = new JObject();
            message.email = _email;
            message.frame = PackFrame(frame);
            
            return message.ToString();
        }

        static private String SendMessage(String url, String json)
        {
            var httpWebRequest = (HttpWebRequest)WebRequest.Create(url);
            httpWebRequest.ContentType = "application/json";
            httpWebRequest.Method = "POST";

            using (var streamWriter = new StreamWriter(httpWebRequest.GetRequestStream()))
            {
                streamWriter.Write(json);
            }

            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
            {
                return streamReader.ReadToEnd();
            }
        }


        public Form1()
        {
            InitializeComponent();

            _capture = VideoCapture.FromCamera(0);
        }

        private async void buttonTemplate_Click(object sender, EventArgs e)
        {
            await Task.Run(() => this.ProcessTemplate());
        }

        private async void buttonAnalysis_Click(object sender, EventArgs e)
        {
            _is_started = true;
            _cts = new CancellationTokenSource();
            try
            {
                await Task.Run(() => this.ProcessAnalysis(), _cts.Token);
            }
            catch (OperationCanceledException)
            {
                _is_started = false;

            }

        }
        
        private void buttonCancel_Click(object sender, EventArgs e)
        {
            _cts.Cancel();
        }
    }
}
