from typing import Tuple

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parsers import summary_parser, Summary


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    #linkedin_url = "fake"
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock = True)

    twitter_username = twitter_lookup_agent(name=name)
    #twitter_username = "fake"
    tweets=scrape_user_tweets(username=twitter_username)

    summary_template = """
        given the information about a person from Linkedin: <linkedin>{information}</linkedin>, and their later twitter
         posts <twitter>{twitter_posts}</twitter>. I want you to create:
        1. A short summary
        2. Two interesting facts about them
        
        Use both information from twitter and LinkedIn
        \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={"format_instructions":summary_parser.get_format_instructions()},
    )

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    #chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    chain = summary_prompt_template | llm | summary_parser

    res:Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})
    print(res)
    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()

    print("Hello LangChain!")

    ice_break_with(name="Eden Marco Udemy")
