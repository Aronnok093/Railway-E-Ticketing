using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace E_TICKET.Models
{
    public class Login
    {   [Required(ErrorMessage =" ")]
        [Display(Name = "Mobile")]
        public string mobile { get; set; }
        [Display(Name = "Password")]
        [Required(ErrorMessage = " ")]
        [DataType(DataType.Password)]
        public string pass { get; set; }
    }
}