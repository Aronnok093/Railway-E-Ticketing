using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace E_TICKET.Models
{
    public class TrainSearchResult
    {   
        public int Train_No {get; set;}
        public int Seat_No { get; set; }
        public String Train_Name {get; set;}
        public String Departure_Station {get; set;}
        public String Arrival_Station {get; set;}
        public String Departure_time {get; set;}
        public String Arrival_Time {get; set;}
        public int Coach_fare {get; set;}
        public String Class {get; set;}
        public String Coach_Name {get; set;}
        public String Ticket_ID { get; set; }

    }
}