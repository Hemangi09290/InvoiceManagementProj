$(document).ready(function(){
	$('[id="id_date"]').attr('readonly','readonly');	
	$('[id="id_date"]').attr('placeholder', 'dd/mm/yyyy');
	$("#id_non_billable_hours").attr('placeholder', 'hh:mm');
	$("#id_billable_hours").attr('placeholder', 'hh:mm');
	$('#submit').click(function(e) {
		console.log(condition());
		if(condition()){

			e.preventDefault();
		}
		else{
			chechkTask();
			$('#entry').submit();
		}
	});


	function condition()
	{
		clear();
		var project_id = document.entry.id_project_id;
		var task = document.entry.id_task;
		var nonbillabletask = document.entry.id_non_billable_task;
		var hours =parseInt($('#id_billable_hours').val().replace(':',''));
		var non_hours =parseInt($('#id_non_billable_hours').val().replace(':',''));
		var date = document.entry.id_date;

		if(valid_project(project_id))
		{
			if (hours || non_hours)
			{
				if (hours)
				{
					if(!valid_task(task)) return true;
				}
				else if(task.value != ""){
					document.getElementById("hourserror").innerHTML="Enter Hours !";
					return true;
				}
				if (non_hours)
				{
					if(!valid_task(nonbillabletask)) return true;
				}
				else if(nonbillabletask.value != ""){
					document.getElementById("nonhourserror").innerHTML="Enter Hours !";
					return true;
				}
				return false;
			}
			else 
			{
				document.getElementById("hourserror").innerHTML="Enter Hours !";
				document.getElementById("nonhourserror").innerHTML="Enter Hours !";
				return true;
			}
		}
		return true;
	}
	function valid_project(project_id)
	{
		if(project_id.value == "")
		{
			document.getElementById("projecterror").innerHTML="Select Project !";
			project_id.focus();
			return false;
		}
		return true;
	}
	function valid_task(task)
	{
		if(task.value == "")
		{
			document.getElementById("taskerror").innerHTML="Enter Task !";
			task.focus();
			return false;
		}
		return true;
	}
	function valid_date(date)
	{
		if(date.value == "")
		{
			document.getElementById("dateerror").innerHTML="Select Date !";
			date.focus();
			return false;
		}
		return true;
	}

	function valid_hours(hours)
	{
		if(hours.value == "")
		{
			document.getElementById("hourserror").innerHTML="Enter Hours !";
			hours.focus();
			return false;
		}
		else
		{
			if(valid_time(hours,"hourserror"))
			{
				return false;
			}
			return true;
		}
	}
	function valid_non_hours(non_hours)
	{
		if(non_hours.value == "")
		{
			document.getElementById("nonhourserror").innerHTML="Enter Hours !";
			non_hours.focus();
			return false;
		}
		else
		{
			if(valid_time(non_hours,"nonhourserror"))
			{
				return false;
			}
			return true;
		}
	}

	function valid_time(hours,hourid)
	{
		re = /^(\d{1,2}):(\d{2})([ap]m)?$/; 
		if(hours.value != '') 
		{ 
			if(regs = hours.value.match(re)) 
			{ 
				if(regs[3]) 
				{ 
	// 12-hour value between 1 and 12 
	if(regs[1] < 1 || regs[1] > 12) 
	{ 
		document.getElementById(hourid).innerHTML="Invalid value for hours: " + regs[1]; 
		hours.focus(); 
		return true; 
	} 
} 
else 
{
		 // 24-hour value between 0 and 23 
		 if(regs[1] > 23) 
		 { 
		 	document.getElementById(hourid).innerHTML="Invalid value for hours: " + regs[1]; 
		 	hours.focus(); 
		 	return true; 
		 } 
		} // minute value between 0 and 59 
		if(regs[2] > 59) 
		{ 
			document.getElementById(hourid).innerHTML="Invalid value for minutes: " + regs[2];
			hours.focus(); 
			return true; 
		} 
	} 
	else 
	{ 
		document.getElementById(hourid).innerHTML="Invalid time format: " + hours.value; 
		hours.focus(); 
		return true; 
	} 
}
return false;
}

function clear()
{
	document.getElementById("dateerror").innerHTML=""
	document.getElementById("taskerror").innerHTML=""
	document.getElementById("nonbillabletaskerror").innerHTML=""
	document.getElementById("hourserror").innerHTML=""
	document.getElementById("nonhourserror").innerHTML=""
	document.getElementById("projecterror").innerHTML=""
}



});