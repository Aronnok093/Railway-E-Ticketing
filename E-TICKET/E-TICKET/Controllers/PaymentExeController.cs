using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace E_TICKET.Controllers
{
    public class PaymentExeController : APIController
    {
        // GET: PaymentExe
        public void Get()
        {
            RunExe();
        }

        public void RunExe()
        { // try
           // {
                var fileName = HttpContext.Current.Server.MapPath("/PaymentGetWay/dist/PaymentGetway.exe");
                Process process = new Process();
                process.StartInfo.RedirectStandardOutput = true;
                process.StartInfo.UseShellExecute = false;
                process.StartInfo.CreateNoWindow = true;
                process.StartInfo.FileName = fileName;
                //process.StartInfo.Arguments = arguments;
                process.StartInfo.WorkingDirectory = HttpContext.Current.Server.MapPath("/PaymentGetWay/");

                process.Start();
                //process.WaitForExit();
            //}catch(Exception ex)
           // {
               // Console.Write(ex.Message);
           // }
        }
    }
}