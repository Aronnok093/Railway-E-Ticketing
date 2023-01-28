using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace E_TICKET.Models
{
    public class ContactUs
    {
        [Required(ErrorMessage = " ")]
        public string name { get; set; }
        [Required(ErrorMessage = " ")]
        public string email { get; set; }
        [Required(ErrorMessage = " ")]
        public string msg { get; set; }
    }
}