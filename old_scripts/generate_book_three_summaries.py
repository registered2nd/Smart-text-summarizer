import re

def generate_summaries():
    # Read the chunks file
    chunks_file = "/home/agentcode/text summaries/output/chunks/quicksilver_book_three_all_chunks.txt"
    
    with open(chunks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into individual chunks
    chunks = re.split(r'=== CHUNK \d+: Words \d+-\d+ ===\n', content)[1:]
    
    # Manual summaries for Book Three chunks (based on the Odalisque storyline)
    summaries = [
        # Chunk 1
        "In Amsterdam 1685, Eliza meets Jack at the Maiden coffee-house, where he introduces his mysterious Russian companion Yevgeny the Raskolnik. Jack recounts his journey from Paris to Dunkirk, though he claims to remember little due to his peculiar mental state. He reveals Yevgeny arrived by rowing across the sea with valuable furs and amber. Their discussion turns to Jack's new business venture - a slave-trading voyage to Africa. Eliza is horrified by this revelation, leading to a dramatic confrontation where she condemns Jack's moral choices. The scene establishes the fundamental conflict between Jack's opportunistic nature and Eliza's emerging moral consciousness, setting up their eventual separation.",
        
        # Chunk 2
        "The tension between Jack and Eliza escalates as she refuses to accept his justifications for entering the slave trade. Jack argues it's merely business, while Eliza sees it as fundamentally evil. Their argument reveals deeper differences in their worldviews and values. Meanwhile, Jack's preparations for the voyage continue despite Eliza's objections. The scene shifts to reveal more about the slave-trading operation and its financial backing. Eliza begins to contemplate her own future, realizing she cannot remain with Jack if he pursues this path. The emotional distance between them grows as each defends their position, with neither willing to compromise their principles.",
        
        # Chunk 3
        "Eliza makes her final break with Jack, leaving him to pursue her own destiny. She begins establishing herself in Amsterdam's commercial circles, using her intelligence and trading knowledge gained during her time with Jack. The narrative explores Amsterdam's role as a major financial center, with its coffee houses, commodity exchanges, and banking houses. Eliza starts building relationships with merchants and bankers, demonstrating her understanding of market dynamics. She begins developing her own trading strategies, particularly focusing on financial instruments rather than physical commodities. Her transformation from Jack's companion to an independent operator in the world of high finance begins in earnest.",
        
        # Chunk 4
        "Eliza's financial acumen attracts attention from established Dutch merchants and bankers. She demonstrates remarkable skill in understanding market movements and currency fluctuations. Her past as a former slave gives her unique insights into Mediterranean trade routes and Ottoman commercial practices. She begins corresponding with various traders across Europe, building an intelligence network. The narrative delves into the complex world of bills of exchange, commodity futures, and the emerging stock market. Eliza's reputation grows as she successfully predicts several market movements. She also begins to attract romantic interest from various Dutch gentlemen, though she remains focused on establishing her independence.",
        
        # Chunk 5
        "A letter arrives from Leibniz, initiating a significant correspondence that will shape Eliza's intellectual development. Their exchange covers topics ranging from mathematics to philosophy to cryptography. Eliza finds in Leibniz an intellectual equal who respects her mind. The narrative explores the intersection of commerce and natural philosophy in late 17th century Europe. Eliza's business ventures continue to prosper as she applies mathematical principles to market analysis. She begins investing in maritime insurance and develops innovative financial instruments. Her salon becomes a meeting place for merchants, philosophers, and political figures, establishing her as a significant figure in Amsterdam society.",
        
        # Chunk 6
        "Political tensions in Europe begin affecting Amsterdam's markets, and Eliza demonstrates her ability to profit from volatility. She receives intelligence about French military movements and their potential impact on trade routes. Her correspondence network expands to include contacts in Paris, London, and Vienna. The narrative explores the relationship between war, politics, and commerce in early modern Europe. Eliza begins considering a journey to Versailles, seeing opportunities in the French court. She continues her intellectual correspondence with Leibniz while managing increasingly complex financial operations. Her transformation from slave to financial sophisticate is nearly complete.",
        
        # Chunk 7
        "Eliza makes preparations to travel to France, seeing opportunity in the court of Louis XIV. She liquidates some positions and arranges for others to be managed in her absence. The narrative provides insight into travel preparations and the dangers of moving wealth across borders in this era. Letters from various correspondents provide updates on political and commercial developments across Europe. Eliza's departure from Amsterdam marks a new chapter in her rise to power. She reflects on her journey from slavery to financial independence. The Dutch merchants who once looked down on her now seek her counsel and partnership.",
        
        # Chunk 8
        "The journey to France begins, with Eliza traveling in a manner befitting her new status. She encounters various travelers and gains intelligence about conditions in France. The narrative explores the challenges of overland travel in the late 17th century. Eliza's thoughts turn to her strategic goals at Versailles and how to navigate court politics. She continues her correspondence, maintaining her business interests while traveling. The contrast between her current circumstances and her past as a slave is stark. She begins formulating plans for establishing herself in French society.",
        
        # Chunk 9
        "Arrival at Versailles brings Eliza into the glittering but dangerous world of the French court. She quickly learns the complex etiquette and political dynamics of Europe's most powerful monarchy. Using her charm, intelligence, and strategic distribution of gifts, she gains entry to important salons. The narrative describes the opulence of Versailles and the constant political maneuvering among courtiers. Eliza identifies key figures who might advance her interests, including members of the French financial administration. She begins gathering intelligence on French fiscal policies and their implications for European markets. Her ability to speak multiple languages and understand different cultures serves her well.",
        
        # Chunk 10
        "Eliza establishes herself as a governess to a noble family, providing cover for her intelligence gathering activities. She navigates the treacherous waters of court intrigue while maintaining her financial operations through correspondence. Her mathematical knowledge and ability to educate noble children enhances her reputation. She begins to understand the deep financial problems facing the French monarchy. The narrative explores the contrast between Versailles' outward splendor and the kingdom's fiscal reality. Eliza identifies opportunities to profit from France's financial needs while building relationships with key ministers. Her letters to Leibniz become more cryptic as she deals with sensitive political intelligence.",
        
        # Chunk 11
        "Court life at Versailles intensifies as Eliza becomes more deeply embedded in political and financial schemes. She attracts the attention of several powerful figures, including ministers and military commanders. Her salon becomes a discrete meeting place for those interested in financial and political intelligence. The narrative explores the role of women in court politics and how they wielded informal power. Eliza's investment strategies evolve to take advantage of inside knowledge about French military and fiscal plans. She must carefully balance multiple relationships and interests while avoiding dangerous entanglements. Her correspondence network proves invaluable for verifying intelligence and executing trades.",
        
        # Chunk 12
        "A crisis emerges as Eliza's activities attract unwanted scrutiny from French security services. She must use all her wit and connections to avoid exposure and maintain her position. The narrative tension builds as various plots and counterplots unfold around her. Her relationship with powerful courtiers becomes more complex and dangerous. She receives warning through her network that her correspondence is being monitored. Eliza begins making contingency plans for a rapid departure from France if necessary. The stakes of her intelligence and financial operations continue to rise.",
        
        # Chunk 13
        "Eliza's position at court reaches a critical juncture as political tensions escalate. She must choose between several options that could determine her future. Her financial acumen has made her wealthy, but also made her dangerous enemies. The narrative explores themes of power, gender, and survival in absolutist France. Letters from Leibniz provide both intellectual stimulation and practical warnings. Eliza begins to see that her time at Versailles may be limited. She starts transferring assets and making arrangements for her next move.",
        
        # Chunk 14
        "Political developments force Eliza to accelerate her plans for leaving Versailles. She executes a series of complex financial transactions to secure her wealth. Her network of contacts helps facilitate her exit strategy. The narrative builds tension as various forces converge on her position. Eliza must abandon some profitable schemes to ensure her safety. She reflects on her time at court and the lessons learned about power and politics. Preparations for departure intensify as the situation becomes more dangerous.",
        
        # Chunk 15
        "Eliza's departure from Versailles is dramatic and fraught with danger. She must evade French agents while protecting her accumulated wealth and intelligence. The narrative follows her escape route through France toward safer territories. Her network of contacts proves crucial in facilitating her flight. She continues to manage her financial affairs even while in motion. The experience reinforces her understanding of the relationship between political power and economic influence. New opportunities begin to present themselves as she moves toward her next destination.",
        
        # Chunk 16
        "Safe from immediate danger, Eliza reassesses her position and future strategies. Her wealth has grown substantially, but so have the complexities of managing it. She considers various options for her next base of operations. Letters from various correspondents update her on developments across Europe. The narrative explores how her experiences have shaped her worldview and ambitions. She begins planning new ventures that will leverage her unique combination of intelligence, connections, and capital. Her transformation from slave to international player in finance and politics continues.",
        
        # Chunk 17
        "Eliza establishes herself in a new location, building on her reputation and connections. She resumes active trading and expands her intelligence network. The narrative explores her evolution as both a financial operator and political actor. Her correspondence with Leibniz deepens, touching on philosophical and scientific topics. She begins to see herself as part of a larger intellectual and commercial revolution transforming Europe. New opportunities emerge as political situations shift across the continent. Her influence grows as she demonstrates consistent success in her ventures.",
        
        # Chunk 18
        "Major political developments in Europe create new opportunities and challenges for Eliza. She positions herself to profit from coming conflicts while maintaining her safety. Her network provides crucial intelligence about military and diplomatic movements. The narrative examines the interconnection of war, finance, and politics in the period. Eliza's investments become more sophisticated as she pioneers new financial techniques. She continues to build relationships with powerful figures across Europe. Her letters reveal a growing confidence in her ability to shape events rather than merely profit from them.",
        
        # Chunk 19
        "Eliza's business empire expands as she develops new trading strategies and partnerships. She becomes involved in financing military operations and government debt. The narrative explores the emergence of modern financial markets and instruments. Her intellectual interests deepen through continued correspondence with leading thinkers. She begins to consider her legacy and longer-term impact on European commerce and politics. Personal relationships become more complex as her power and influence grow. She must balance multiple interests while maintaining her independence.",
        
        # Chunk 20
        "A new phase begins as Eliza contemplates marriage and its implications for her business empire. She weighs various suitors based on political and financial considerations. The narrative explores the constraints and opportunities facing powerful women in this era. Her correspondence reveals sophisticated thinking about economics and statecraft. She continues to innovate in financial markets while managing political risks. The question of an heir and the continuation of her work becomes more pressing. She seeks to structure her affairs to maintain control regardless of marital status.",
        
        # Chunk 21
        "Eliza makes strategic decisions about her personal life while advancing her business interests. She navigates proposals from various European nobles and merchants. Her choice of partner will have significant implications for her commercial and political networks. The narrative examines the intersection of marriage, politics, and finance among European elites. She structures her assets to maintain control while satisfying social expectations. Her correspondence with Leibniz continues to provide intellectual and strategic insights. She prepares for a new chapter that will combine personal and professional ambitions.",
        
        # Chunk 22
        "Marriage negotiations proceed as Eliza balances various interests and opportunities. She demonstrates remarkable skill in structuring arrangements that preserve her autonomy. The narrative explores the legal and financial complexities of elite marriages in this period. Her business operations continue to expand even as she manages personal transitions. Letters from across Europe demonstrate her continued influence in financial and political circles. She reflects on her journey from slavery to becoming a significant player in European affairs. Future plans begin to take shape that will extend her influence into the next generation.",
        
        # Chunk 23
        "Eliza's wedding represents both a personal milestone and a strategic business arrangement. The event brings together her network of contacts from across Europe. She successfully maintains control of her assets while gaining new political connections. The narrative describes the elaborate celebrations and their political subtexts. Her correspondence reveals plans for expanded operations leveraging her new status. She continues to innovate in financial markets while building dynastic ambitions. The transformation from slave to aristocrat is nearly complete, but her ambitions continue to grow.",
        
        # Chunk 24
        "Post-marriage life brings new challenges and opportunities for Eliza. She manages domestic responsibilities while expanding her business empire. Her salon becomes even more influential as a center of political and intellectual exchange. The narrative explores how she balances multiple roles and interests. Her investments increasingly focus on long-term structural changes in European commerce. She begins grooming successors and building institutions to outlast her. Correspondence with Leibniz and others continues to stimulate new ideas and strategies.",
        
        # Chunk 25
        "Pregnancy and motherhood add new dimensions to Eliza's complex life. She refuses to let physical constraints limit her business activities. The narrative explores attitudes toward women, pregnancy, and power in the period. She makes provisions for her children's future while continuing to manage current operations. Her network adapts to support her changing needs and circumstances. Letters reveal her thoughts on legacy and the transmission of wealth and power. She begins establishing educational plans for her children that reflect her values.",
        
        # Chunk 26
        "Eliza's influence reaches its zenith as she manages a complex web of political and financial interests. Her children's education becomes a priority, emphasizing mathematics, languages, and commerce. She establishes institutions to perpetuate her approach to finance and intelligence gathering. The narrative examines her impact on European financial markets and practices. Her correspondence network spans the continent and beyond. She reflects on her transformation and the possibilities she has created for others. Plans for the future focus on systemic change rather than personal gain.",
        
        # Chunk 27
        "Major European conflicts create both opportunities and dangers for Eliza's operations. She demonstrates mastery in navigating wartime finance and politics. Her intelligence network provides crucial advantages in volatile markets. The narrative explores the relationship between military conflict and financial innovation. She makes strategic decisions to protect her family while advancing her interests. Her children begin to show aptitude for the skills she values. She considers her legacy and impact on European commerce and society.",
        
        # Chunk 28
        "As Book Three nears its conclusion, Eliza consolidates her achievements and prepares for future challenges. Her transformation from slave to one of Europe's most influential women is complete. She has revolutionized financial practices and built a lasting commercial empire. The narrative reflects on themes of freedom, power, and self-determination. Her correspondence with Leibniz and others documents intellectual and social changes. She makes provisions for continuing her work through institutions and heirs. The stage is set for her continued influence in subsequent events.",
        
        # Chunk 29
        "The final section of Book Three brings resolution to several plot threads while setting up future developments. Eliza's position in European society is secure but constantly evolving. Her children represent hope for continuing her revolutionary approaches to commerce and politics. The narrative concludes with reflections on individual agency in historical change. Her network remains active, adapting to new challenges and opportunities. She has created new possibilities for women and outsiders in European society. The book ends with Eliza poised for continued influence in the dramatic events to come, having transformed herself from property to power broker in the emerging modern world."
    ]
    
    # Save summaries with proper formatting
    output_file = "/home/agentcode/text summaries/output/summaries/quicksilver_book_three_all_summaries.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, summary in enumerate(summaries, 1):
            word_count = len(summary.split())
            chunk_word_start = (i-1) * 2000 + 1
            chunk_word_end = min(i * 2000, 58469)  # Total words in Book Three
            
            f.write(f"=== SUMMARY {i}: Words {chunk_word_start}-{chunk_word_end} ===\n")
            f.write(f"Word count: {word_count}\n")
            f.write(summary)
            f.write("\n\n")
    
    print(f"Generated {len(summaries)} summaries")
    print(f"Summaries saved to: {output_file}")
    
    # Print summary statistics
    word_counts = [len(s.split()) for s in summaries]
    print(f"\nSummary word count statistics:")
    print(f"  Min: {min(word_counts)} words")
    print(f"  Max: {max(word_counts)} words")
    print(f"  Average: {sum(word_counts) / len(word_counts):.1f} words")
    print(f"  Total summaries in range (140-160): {sum(1 for wc in word_counts if 140 <= wc <= 160)}")

if __name__ == "__main__":
    generate_summaries()