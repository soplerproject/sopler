//Item menu button effects
function itemoptions_effects(checked,mobile,button,itempk){
	
	var collapseID;
	var ID;
	if(checked){
		ID = itempk;
		collapseID = ("#collapse-").concat(button,"-",ID);
	}else{
		ID = ("unchecked-").concat(itempk);
		collapseID = ("#collapse-").concat(button,"_",ID);
	}
	if(mobile){
		ID = ID.concat("-mob");
	}
	//check if collapse is open or hidden
	if($(collapseID).attr("aria-expanded") == 'true'){
		$(collapseID).collapse('toggle');
		//check which button is used
		if(button == "edit"){
			//check if mobile panel is used
			if (mobile == 0){
				$("#edit-" + ID).addClass('col-sm-4').removeClass('col-sm-12');
			}
			//check if this is a checked/unchecked item
			if(checked){
				$('#info-' + ID).fadeIn("slow");
			}else{
				$('#duedate-' + ID).fadeIn("slow");
			}
		}else if( button == "duedate" || button == "info"){
			if (mobile == 0){
				$("#"+button+"-" + ID).addClass('col-sm-6 col-sm-push-1').removeClass('col-sm-12');
			}
			$("#edit-" + ID).fadeIn("slow");
		}
		$('#priority-' + ID).fadeIn("slow");
		$('#lock-' + ID).fadeIn("slow");
		$("#delete-" + ID).fadeIn("slow");
	}else{
	//the same for the hidden state of collapse
		$('#priority-' + ID).fadeOut("slow");
		$('#lock-' + ID).fadeOut("slow");
		$('#delete-' + ID).fadeOut("slow");
		if( button == "edit" ){
			if(checked){
				$('#info-' + ID).fadeOut("slow");
			}else{
				$('#duedate-' + ID).fadeOut("slow");
			}
			if (mobile == 0){
				$('#edit-'+ ID).addClass('col-sm-12').removeClass('col-sm-4');
			}
		}else if( button == "duedate" || button == "info" ){
			$('#edit-' + ID).fadeOut("slow");
			$('#delete-' + ID).fadeOut("slow");
			if(mobile == 0){
				$("#"+button+"-" + ID).addClass('col-sm-12').removeClass('col-sm-6 col-sm-push-1');	
			}	
		}
		setTimeout(function () {$(collapseID).collapse('toggle')}, 800);
	}
};
