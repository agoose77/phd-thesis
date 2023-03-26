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

(olab:motivations)=

# Motivations

+++

The identification of the SARS-COV-2 virus in 2019 marked the onset of an unprecedented period of social and economic disruption across the global community. Its impact has been felt in the majority of countries around the world, both in terms of the real-terms consequences of wide-spread infection, and the subsequent public health interventions in pursuit of elimination or suppression. Within the domain of Higher Education, which has placed a particular importance upon in-person learning and interaction, the complex ongoing challenges associated with the COVID-19 pandemic have placed significant burden upon educators and their institutions {cite:ps}`watermeyer_covid-19_2021`.

+++

At the University of Birmingham, a central aspect of the Nuclear Physics teaching provision is the availability of undergraduate laboratories. Over the course of the teaching semester, students enrolled in the appropriate modules are given the opportunity to learn the fundamentals of practical nuclear physics, including
- the principles which underpin the measurement of radiation, 
- the process of building and testing radiation experiments,
- practices and procedures involved in working with radioactive sources,
- the analytical techniques required to extract physics from laboratory measurements.

+++

The specialised nature of the laboratory sessions in which these skills are taught imposes rigid constraints on the kinds of accommodations that can be made in light of University  public health measures e.g. occupancy limits, staffing availability, and ventilation requirements. Several experiments that undergraduates are expected to undertake include fundamentally immovable apparatus, such as a {math}`8\,\text{m}^3` graphite stack for neutron moderation, or a 150 L water bath used for neutron activation experiments.

The detector equipment used to observe and measure incident radiation is typically fragile, bulky, and extremely expensive, such that undergraduates are not expected to move such equipment within the laboratory. The radioactive sources used within the various experiments are also controlled substances; requiring significant care during handling, preparatory safety training, and diligent monitoring to ensure that the sources are properly accounted for at all times. These factors conspire together such that conventional approaches to mitigating COVID-19 risks during the pandemic, such as the introduction of a "two meter rule", or reducing teaching group sizes, represent impractical solutions in the context of the nuclear laboratory {cite:ps}`jones_two_2020`.

+++

Unlike other areas of the taught programmes such as lectures, in which provisions for distance learning (such as Panopto) were already in-use within the undergraduate teaching programs before the pandemic, no such solutions could be found to facilitate the development of practical laboratory skills in the domain of Nuclear Physics {cite:ps}`jandric_teaching_2021`. To address this challenge for the new and existing students impacted by the COVID-19 pandemic, an Online nuclear LABoratory (OLAB) was developed by a team of postgraduate nuclear physics students at the University of Birmingham. The objectives of this project were to implement an online learning resource which 
   - minimises the impact of digital inequality
   - scales to meet the demand of the existing and future student cohorts
   - provides an extensible platform upon which to develop new course material
   - integrates with the University E-Learning platform(s)
   - leverages existing, open-source technologies and
   - facilitates content-first development
