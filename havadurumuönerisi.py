import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')
#anlık

@bot.command()
async def hava_durumu (ctx, *, sehir: str):
    api_key = "ff4d0f71153fc14f03f0ef1410af08a9" 
    url = f'http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr'
    yanit = requests.get(url)
    veri = yanit.json()

    if yanit.status_code == 200:
        hava_durumu_aciklama = veri['weather'][0]['description']
        sicaklik = veri['main']['temp']


        if hava_durumu_aciklama == 'yağmurlu':
            giyim_tipi = 'Yağmurluk ve şemsiye kullanmayı unutmayın!'
        elif hava_durumu_aciklama == 'karlı':
            giyim_tipi = 'Sıcak ve kalın giysiler giyin, kar botları kullanın.'
        elif sicaklik >= 35:
            giyim_tipi = 'Denize girin şort vb. giyin, şapka ve güneş kremi kullanın.'    
        elif sicaklik >= 25:
            giyim_tipi = 'Hafif ve serin giysiler tercih edin, şapka ve güneş kremi kullanın.'
        elif sicaklik >= 15:
            giyim_tipi = 'Hafif bir ceket veya kazak giyin, şemsiye taşıyın.'
        elif hava_durumu_aciklama == 'fırtına':
            giyim_tipi = 'Gerekmedikçe evden çıkmayın camları,kapıları kapatınız.'
        await ctx.send(f'{sehir} şehri için hava durumu: {hava_durumu_aciklama.capitalize()},\nSıcaklık:{sicaklik}°C,\ngiyim_tipi:{giyim_tipi}')
    else:
        await ctx.send('Belirtilen şehir bulunamadı. Lütfen geçerli bir şehir adı girin.')

#saatlik

@bot.command()
async def saatlik_hava_durumu(ctx, *, sehir: str):
    api_key = "ff4d0f71153fc14f03f0ef1410af08a9" 
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={sehir}&appid={api_key}&units=metric&lang=tr'
    yanit = requests.get(url)
    veri = yanit.json()

    if yanit.status_code == 200:
        saatlik_hava_durumu_tahminler = veri['list'][:7]  #  7 farklı saat tahmini al

        giyim_tavsiyeleri = []
        for tahmin in saatlik_hava_durumu_tahminler:
            tarih = tahmin['dt_txt']
            hava_durumu_aciklama = tahmin['weather'][0]['description']
            sicaklik = tahmin['main']['temp']

            giyim_tipi = ''
            if hava_durumu_aciklama == 'Rain':
                giyim_tipi = 'Yağmurluk ve şemsiye kullanmayı unutmayın!'
            elif hava_durumu_aciklama == 'Snow':
                giyim_tipi = 'Sıcak ve kalın giysiler giyin, kar botları kullanın.'
            elif sicaklik >= 35:
                giyim_tipi = 'Denize girin, şort vb. giyin, şapka ve güneş kremi kullanın.'
            elif sicaklik >= 25:
                giyim_tipi = 'Hafif ve serin giysiler tercih edin, şapka ve güneş kremi kullanın.'
            elif sicaklik >= 15:
                giyim_tipi = 'Hafif bir ceket veya kazak giyin, şemsiye taşıyın.'
            elif hava_durumu_aciklama == 'Fog':
                giyim_tipi = 'Dikkatli olun, sisli hava koşullarında açık renkli giysiler tercih edin.'

            giyim_tavsiyeleri.append(f'{tarih}: {hava_durumu_aciklama.capitalize()}, Sıcaklık: {sicaklik}°C - Giyim Tavsiyesi: {giyim_tipi}')

        await ctx.send(f'{sehir} şehri için haftalık hava durumu ve giyim tavsiyeleri:\n\n' + '\n'.join(giyim_tavsiyeleri))
    else:
        await ctx.send('Belirtilen şehir bilgisi bulunamadı. Lütfen geçerli bir şehir adı girin.')


bot.run("MTE2NzUzMTc4OTExMjMyNDA5Ng.GfGZT-.5Sv64EgstbZNhinlGmVOoJ1Ypo9bbpVP8XIf2g")   