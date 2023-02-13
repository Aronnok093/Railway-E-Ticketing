using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace E_TICKET.Controllers
{
    public class TimeDateController : Controller
    {
      
        public string Date()
        {
            DateTime dt= DateTime.Now.AddDays(1);
            string dateTime = dt.ToShortDateString();
            return dateTime;
        }
    }
}