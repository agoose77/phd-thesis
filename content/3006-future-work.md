---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Future Work

+++

It was discussed in {numref}`olab:content` that the provisional O-Lab deployment was designed with reduced scope in order to meet the requirements of the academic timetabling. these constraints. Yet, in {numref}`olab:virtual-laboratories`, it was established that the wider landscape available to virtual laboratory design is much broader; the decision to replicate in-person experiments is both a practical decision _and_ an educational one. Whilst the primary goal of this early O-Lab deployment was to facilitate the student laboratory provision during the semesters disrupted by public health measures, subsequent investigations could be designed to further explore the utility of a virtual nuclear laboratory in both hybrid and dedicated contexts. In order to evaluate the value of such a proposal, it would be necessary to predetermine the scope of a subsequent pilot study, and establish the criteria by which success can be measured. Both educators and students are stakeholders in laboratory work, and it would be of fundamental importance to establish a dialogue with these groups in the wake of this O-Lab deployment to determine those aspects which proved of value to students. At the same time, educators should be encouraged to provide feedback as to the impact that the virtual format of these laboratories had upon student engagement and understanding, particularly in relation to assessed material such as lab reports. During this preliminary trial, a feedback form was designed in order to assess student sentiment towards the trial, but was not released to students following technical errors. Such feedback would prove invaluable in directing future development of the O-Lab platform.

+++

In addition to a broader remit, a subsequent iteration on the O-Lab platform could look to expand its scope for student interaction. O-Lab was designed upon a platform that could be extended to meet future need, such as student analyses. In the majority of experiments there is a need to analyse data, which is conventionally done with in-house software. Future development could provide students with a JupyterLab instance, and implement additional widgets to export data from the O-Lab frontend to these sessions in order to facilitate further investigation. It is of growing importance to be able to perform analysis work using programming languages such as Python; providing an ability for students to leverage these skills within a virtual laboratory would provide both a mechanism to reinforce student understanding and cross-discipline knowledge. Additional JupyterLab plugins such as `jupyterlab-preview` enable integration of voila-backed dashboards within the JupyterLab environment (see {numref}`jupyterlab-voila-preview`).

+++

:::{figure} image/jupyterlab-voila-preview.png
:name: jupyterlab-voila-preview
:width: 512px
:align: center

Screenshot of the Voila preview panel running in JupyterLab courtesy of the `jupyterlab-preview` extension. With this extension, customised dashboards can be opened by the user, whilst conventional cellular notebooks can also be edited and run.
:::

+++

Students were able to engage with remote demonstrators during the O-Lab trial period using the Zoom video-conferencing software. JupyterHub plugins such as `jupyter-videochat` could be added to the JupyterHub deployment in order to reduce the barrier to engaging with demonstrators (see {numref}`jupyterlab-video-chat`) {cite:ps}`noauthor_jupyter-videochat_nodate`. It would also then be easier for students to form breakout rooms to work with peers on group projects. This would be increasingly useful as the scope of the O-Lab project grows, where the logistics concerning organising Zoom meetings could be circumvented in favour of drop-in sessions facilitated by the Hub plugin.

JupyterLab also implements support for collaborative editing. As part of a remote-first workflow, teaching assistants could utilise such a feature to work with students to resolve problems with their analysis. The standard working practices in the practical laboratory are designed around resource limitations; students are often tasked with working in pairs. The O-Lab pilot demonstrated that this was no longer a practical issue, and introduced the ability for students to work individually. Therefore, the collaborative features of JupyterLab could be employed to permit students collaborate on an analysis. Alongside a push towards building and publishing reports as interactive documents (notebooks), this kind of shared editing provides the opportunity for deeper collaboration than conventional pen-and-paper based workflows.

+++

:::{figure} image/jupyterlab-video-chat.png
:name: jupyterlab-video-chat
:width: 512px
:align: center

Screenshot of the Jitsi video chat panel running in JupyterLab courtesy of the `jupyterlab-videochat` extension. Jitsi provides the conventional video-conferencing features that students are already familiar with, conveniently integrated with the JupyterLab application. 
:::

+++

The Apple iOS operating system popularised the concept of skeumorphic design; making items resemble their real-world counterparts. Though there is continuing debate as to whether skeumorphism aids retention and learning, there is evidence to suggest that the _affordances_ (ability to determine as-yet unseen behaviour from visual cues) it provides reduce cognitive overhead through familiar metaphors {cite:ps}`oswald_flat_2014`. The real-world equipment that O-Lab imitates, such as the high-voltage amplifiers, could be extended to acknowledge this design trend. One approach would be to retain the existing data-oriented user interface, and design a visual widget that represents the equipment state (e.g. the front display panel of the HV amplifier). Another, more involved approach would be to replace the form input fields with an entirely skeumorphic UI, e.g. replacing sliders with control knobs. As a component of these approaches, additional development could be spent in the direction of teaching students how to assemble an experiment in an interactive manner. As these are inherently visual changes, considerable effort would be required to implement and validate the approaches.

+++

<!-- - Jitsi integration
- JupyterLab breakout
- Collaborative JupyterHub
- skeumorphism with UX, or skeumorphic view of sliders?
- Dead time -->
