using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace E_TICKET.Models
{
    public class TrainInformation
    {
        public int Train_No { get; set; }
	    public string Train_Name { get; set; }
        public string Offday { get; set; }
        public string Departure_Station{ get; set; }
        public string Departure_time { get; set; }
        public string Arrival_Station { get; set; }
	    public string Arrival_Time{ get; set; }
    }
}