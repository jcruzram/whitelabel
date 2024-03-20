$(document).ready(function() {
    if(frappe.ui.OnboardingTour){ 
        
        class CustomOnboardingTour extends frappe.ui.OnboardingTour {
            constructor() {
                super(); // Llama al constructor de la clase base
                // this.all_tours();
            }
            async all_tours(){
                const entries = [
                    "User List Tour",
                    "Users Workspace Tour",
                    "Sales Invoice",
                    "Main Workspace Tour",
                    "Item General",
                    "Print Format",
                    "Company",
                    "Doctype",
                    "Custom Field",
                    "Quotation",
                    "Customer",
                    "Letter Head",
                    "Item",
                    "Asset",
                    "Stock Reconciliation",
                    "Stock Entry",
                    "Warehouse",
                    "Purchase Receipt",
                    "Asset Category",
                    "Sales Taxes and Charges Template",
                    "Stock Settings",
                    "Purchase Order",
                    "Material Request",
                    "Buying Settings",
                    "Sales Order",
                    "Selling Settings",
                    "Accounts Settings",
                    "Purchase Invoice"
                ];
                let arrSteps = [];
                let arrTitles = [];
                
                for (let i = 0; i < entries.length; i++) {
                    var tour = await frappe.db.get_doc("Form Tour",entries[i]);
                    tour.steps.forEach((step) => {
                        arrSteps.push(step.description);
                        arrTitles.push(step.title);
                        // console.log(step.description);
                        // console.log(step.title);
                    });
                }
                // Join the entries into a single string with line breaks
                const content = arrSteps.join('\n');
                const content1 = arrTitles.join('\n');
                // Specify the file path where you want to create the text file
                console.log(content);
                console.log(content1);
                const stepsPath = 'steps.txt';
                const titlesPath = 'titles.txt';
                // Write the content to the file
                fs.writeFileSync(stepsPath, content);
                fs.writeFileSync(titlesPath, content1);
            }

            init_driver() {
                this.driver = new frappe.Driver({
                    className: "frappe-driver",
                    allowClose: false,
                    padding: 10,
                    overlayClickNext: false,
                    keyboardControl: true,
                    nextBtnText: __("Next"),
                    prevBtnText: __("Previous"),
                    closeBtnText: __("Close"),
                    opacity: 0.5,
                    onHighlighted: (step) => {
                        frappe.ui.next_form_tour = step.options.step_info?.next_form_tour;
                        const wait_for_node = setInterval(() => {
                            if (!step.popover.node) return;
                            if (step.options.step_info?.offset_x) {
                                step.popover.node.style.left = `${
                                    step.popover.node.offsetLeft + step.options.step_info.offset_x
                                }px`;
                            }
                            if (step.options.step_info?.offset_y) {
                                step.popover.node.style.top = `${
                                    step.popover.node.offsetTop + step.options.step_info.offset_y
                                }px`;
                            }
                            if (step.popover.node.offsetLeft < 0) {
                                step.popover.node.style.minWidth = "200px";
                                step.popover.node.style.maxWidth = `${
                                    350 + step.popover.node.offsetLeft
                                }px`;
                                step.popover.node.style.left = "0px";
                            }
                            if (step.popover.closeBtnNode) {
                                step.popover.closeBtnNode.onclick = () => {
                                    this.on_finish && this.on_finish();
                                    !frappe.boot.user.onboarding_status[this.tour.name] &&
                                        (frappe.boot.user.onboarding_status[this.tour.name] = {});
                                    frappe.boot.user.onboarding_status[this.tour.name].is_complete = true;
                                    if (!this.driver.hasNextStep()) {
                                        frappe.boot.user.onboarding_status[
                                            this.tour.name
                                        ].all_steps_completed = true;
                                    }

                                    frappe.call({
                                        method: "frappe.desk.doctype.form_tour.form_tour.update_user_status",
                                        args: {
                                            value: JSON.stringify(frappe.boot.user.onboarding_status),
                                            step: JSON.stringify(step.options.step_info),
                                        },
                                    });
                                };
                            }
                            clearInterval(wait_for_node);
                        }, 300);
        
                        // focus on first input.
                        // TODO : later add option to select which input to focus as well.
                        const $input = $(step.node).find("input").get(0);
                        if ($input) frappe.utils.sleep(200).then(() => $input.focus());
                    },
                });
            }
                    
            async init({ tour_name, start_step }) {
                this.tour = await frappe.db.get_doc("Form Tour", tour_name);
                this.translate_steps();
                this.init_driver();
                this.build_steps();
                this.update_driver_steps();
                if (!this.tour.track_steps) {
                    start_step = 0;
                }
                this.start(start_step);
            }
            
            translate_steps(){
                this.tour.steps.forEach((step) => {
                    step.description = __(step.description);
                    step.title = __(step.title);
                    console.log(step.description);
                    console.log(step.title);
                });
            }
        };
        
        frappe.ui.OnboardingTour = CustomOnboardingTour;
    }else{
    }
});