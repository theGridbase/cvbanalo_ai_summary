class PreDefinedPrompts:
    @staticmethod
    def system_content(tone, character_limit):
        prompt = f"""
            Craft a compelling, concise, and impactful professional summary for a CV or resume. 
            The summary should emphasize key accomplishments, job roles, and relevant skills, 
            aligning with industry standards and optimizing for readability.

            Guidelines:
            1. Begin with an action verb to reflect strong, decisive contributions.
            2. Avoid the use of pronouns or referring to the user directly.
            3. Highlight measurable outcomes or specific achievements.
            4. Use relevant keywords tied to the job position and industry.
            5. Maintain a {tone} tone, balancing professionalism with engagement.
            6. Keep the summary within {character_limit} characters.
        """
        return prompt

    @staticmethod
    def summary_user_content(job_title, experience, technical_skills, soft_skills, key_achievements=None):
        prompt = f"""
            Based on the following information, generate a resume summary that reflects a strong, impactful professional profile.
            JOB DESCRIPTION:
            - Title: {job_title}
            - Experience: {experience} years
            - Technical Skills: {', '.join(technical_skills)}
            - Soft Skills: {', '.join(soft_skills)}
        """
        if key_achievements:
            prompt += f"- Key Achievements: {', '.join(key_achievements)}"
        return prompt

