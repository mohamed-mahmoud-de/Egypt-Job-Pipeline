import requests
from bs4 import BeautifulSoup


def extract():
    
    jobs = []
    
    url = f"https://wuzzuf.net/search/jobs/?q=internships&a=hpb&"
    response = requests.get(url)
        
    if response.status_code != 200:
        print(f"Failed to fetch page")
        return jobs
        
    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("div", class_="css-pkv5jc")
    if not job_cards:
        print("No more job cards found, ending extraction.")
        return jobs
        
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
        job_id = link

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "date_posted": date_posted,
            "job_type": ", ".join(job_types),
            "link": link,
            "job_id": job_id
        })
    return jobs



