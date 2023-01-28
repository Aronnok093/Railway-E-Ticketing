using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace E_TICKET.Models
{
    public class Resister
    {
        public string id { get; set; }
        [Required(ErrorMessage = " ")]
        [Display(Name = "Name")]
        public string name { get; set; }
        [Required(ErrorMessage = " ")]
        [Display(Name = "Email")]
        public string email { get; set; }
        [Required(ErrorMessage = " ")]
        [Display(Name = "Mobile")]
        public string mobile { get; set; }
        [Required(ErrorMessage = " ")]
        [Display(Name = "Password")]
        public string pass { get; set; }
        [Required(ErrorMessage = " ")]
        [Display(Name = "NID")]
        public string nid { get; set; }
    }
}