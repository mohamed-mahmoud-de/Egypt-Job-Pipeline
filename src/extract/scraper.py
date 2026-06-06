import requests
from bs4 import BeautifulSoup





def scrape_jobs():
    
    start = 0
    jobs = []
    
    while True:
        
        url = f"https://wuzzuf.net/search/jobs/?q=internships&start={start}&a=hpb&"
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="css-ghe2tq")
        

        for card in job_cards:
            title = card.find("h2").find("a").text.strip()
            company_div = card.find("div", class_="css-1k5ee52")
            company = company_div.find("a").text.strip().rstrip("-").strip()
            location_span = company_div.find("span")
            location = location_span.text.strip() if location_span else "N/A"
            date_posted = "N/A"
            for div in company_div.find_all("div"):
                if "ago" in div.text:
                    date_posted = div.text.strip()
                    break
            job_types = [a.text.strip() for a in card.find_all("a", class_="css-a85cz4")]
            link = "https://wuzzuf.net" + card.find("h2").find("a")["href"]

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "date_posted": date_posted,
                "job_type": ", ".join(job_types),
                "link": link
            })
        
        start += 1    
        if not job_cards:
            break

    return jobs
        
        
           
    
    
    

