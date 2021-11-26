PennController.ResetPrefix(null); // Shorten command names
var showProgressBar = false;
DebugOff();

Sequence('pid_check', 'consent', 'caregiver_instructions', 'init', 'child_welcome', 'instructions', 'practice1', 'practice', 'progress1', 'quest1', 'images', 'upload', 'finish');
//Sequence('pid_check', 'init', 'images', 'upload', 'finish');

InitiateRecorder('https://l2t-umd-dmsp.xyz/info.php').label('init');

// ID: ABCD
//    A = 0 (AAE), 1 (GAE)
//    B = 0-4 (Which csv #) [Necessary?]
//    CD = ID #

var img_path = 'https://l2t-umd-dmsp.xyz/images/';
var aud_path = 'https://l2t-umd-dmsp.xyz/audio/';
var csv_path = 'https://l2t-umd-dmsp.xyz/csv/';

var pid_text = prompt('Please enter your 4 digit Participant ID (eg. 0000)', '');
var pid = pid_text.match(/^([0,1])([0-5])(\d{2})$/);
var dialect = pid[1] == 0 ? 'AAE' : 'GAE';
var csv_num = pid[2];
var id = pid[3];

newTrial('pid_check',
    defaultText.center().print(),

    newText('pid', pid_text),

    getText('pid').test.text(/^[0,1][0-5]\d{2}$/).success(
        newText('Is this correct?'),

        newButton('leftbut', 'Reload').callback(newFunction(() => location.reload()).call()).center().print(),

        newButton('rightbut', 'Next').center().print().wait(),
        
        newVar('pid#', pid).log()
    ).failure(
        newText('Invalid Participant ID. Please click the button to reload the page.'),

        newButton('reload', 'Reload').callback(newFunction('f2', () => location.reload()).call()).center().print().wait()
    )
).log('dialect', dialect).log('csv_num', csv_num).log('id', id).log('csv', csv);

newTrial('consent',
    defaultText.center().print(),
    newText('Please press next after you complete the form'),
    newFunction('cons', () => {
        var ifrm = document.createElement('iframe');
        ifrm.setAttribute('src', 'https://form.jotform.com/211945209228153');
        ifrm.style.width = '60vw';
        ifrm.style.height = '75vh';
        ifrm.style.marginLeft = '20vw';
        ifrm.style.marginTop = '9vh';
        ifrm.setAttribute('id', 'cons');
        document.body.appendChild(ifrm);
    }).call(),

    newButton('consbut', 'Next').center().print().wait(),

    newFunction('rem_cons', () => {
        document.getElementById('cons').remove();
    }).call()
);

newTrial('caregiver_instructions',
    defaultText.center().print(),
    newText('Caregiver Instructions'),
    newText('Welcome!'),
    newText('Here are tips to play this game:'),
    newText(' - Seat your child directly in front of the computer screen'),
    newText(' - Do not provide your child with any answers'),

    newButton('next', 'Next').center().print().wait(),

    clear(),

    newText('Webcam Instructions'),
    newText('On the next page, you will be given instructions to activate the webcam for this game.'),
    
    newButton('next2', 'Next').center().print().wait() 
);

newTrial('child_welcome',
    defaultText.center().print(),
    newText('Welcome!'),
    newText('Press the space bar to start the game'),
    
    newAudio('Welcome_Child_Instructions', aud_path + 'Welcome_Child_Instructions.mp3').play().wait().log(),
    newTimer('wait', 200).start().wait(),

    newImage('space_img', img_path + 'spacebar.jpg').center().print(),

    newTimer('wait2', 500).start().wait(),
    
    newKey(' ').wait()
);

newTrial('instructions', 
    defaultText.center().print(),
    newText('Game Instructions'),
    newText('Your job is to rescue your space crew and collect missing spaceship items.'),
    newText('You will hear instructions from a space commander.'),
    newText('Listen carefully and tell me the color box around the picture that best matches what you hear.'),
    newText(' '),
    
    newImage('intro', img_path +  'IntroExperimentDisplayScreen_a.jpg').center().print(),
    
    newAudio('GameInstructionsScreen', aud_path + 'GameInstructionsScreen.mp3').play().wait().log(),

    newKey(' ').wait()
);

var csv = dialect == 'AAE' ? 'randomized_stimuli_AAE'+ csv_num + '.csv' : 'randomized_stimuli_GAE'+ csv_num + '.csv';

newTrial('practice1',

    newImage('topleft', img_path + 'planet_blue_screensideselection.jpg').size(300, 300).print(),
    newImage('topright', img_path + 'planet_orange_screensideselection.jpg').size(300, 300).print(),
    newImage('bottomleft', img_path + 'spaceship_blue_screensideselection.jpg').size(300, 300).print(),
    newImage('bottomright', img_path + 'spaceship_orange_screensideselection.jpg').size(300, 300).print(),
    
    newAudio('Instructions_Colorbox', aud_path + 'Instructions_Colorbox.mp3').play().wait().log(),
    newMediaRecorder('recorder', 'video').log().record(),
    newAudio('Practice_Blueplanet', aud_path + 'Practice_Blueplanet.mp3').play().wait().log(),
    newTimer('wait', 3000).start().wait(),

    newFunction('Practice_Spacebar', () => {
        var audio = new Audio(aud_path + 'Practice_Spacebar.mp3');
        console.log(audio);
        audio.play();
    }).call(),
    newTimer('wait3', 500).start().wait(),
    newButton('space', 'spacebar').center().print(),
    newTimer('wait4', 1000).start().wait(),

    newKey(' ').wait(),

    clear(),
    newTimer('wait5', 200).start().wait(),

    getMediaRecorder('recorder').stop()
).log('trial_type', 'practice');

AddTable('mytable' ,
    'tl,tr,bl,br,audio\n' +
    'planet_blue_screensideselection.jpg,planet_orange_screensideselection.jpg,spaceship_blue_screensideselection.jpg,spaceship_orange_screensideselection.jpg,Find_orangeplanet.mp3\n' + 
    'planet_blue_screensideselection.jpg,planet_orange_screensideselection.jpg,spaceship_blue_screensideselection.jpg,spaceship_orange_screensideselection.jpg,Find_bluespaceship.mp3\n' + 
    'planet_blue_screensideselection.jpg,planet_orange_screensideselection.jpg,spaceship_blue_screensideselection.jpg,spaceship_orange_screensideselection.jpg,Find_orangespaceship.mp3\n' + 
    'astronaut_pink_screensideselection.jpg,spaceship_green_sideselection.jpg,spaceship_pink_screensideselection.jpg,astronaut_green_screensideselection.jpg,practice_pinkastronaut.mp3\n' + 
    'astronaut_pink_screensideselection.jpg,spaceship_green_sideselection.jpg,spaceship_pink_screensideselection.jpg,astronaut_green_screensideselection.jpg,practice_greenastronaut.mp3\n' + 
    'astronaut_pink_screensideselection.jpg,spaceship_green_sideselection.jpg,spaceship_pink_screensideselection.jpg,astronaut_green_screensideselection.jpg,practice_pinkspaceship.mp3\n' + 
    'astronaut_pink_screensideselection.jpg,spaceship_green_sideselection.jpg,spaceship_pink_screensideselection.jpg,astronaut_green_screensideselection.jpg,practice_greenspaceship.mp3\n'
);

Template('mytable' , row =>
    PennController('practice',

        newImage('topleft', img_path + row.tl).size(300, 300).print(),
        newImage('topright', img_path + row.tr).size(300, 300).print(),
        newImage('bottomleft', img_path + row.bl).size(300, 300).print(),
        newImage('bottomright', img_path + row.br).size(300, 300).print(),
    
        newAudio('Instructions_Colorbox', aud_path + 'Instructions_Colorbox.mp3').play().wait().log(),
        newTimer('wait', 1500).start().wait(),
        newMediaRecorder('recorder', 'video').log().record(),
        newAudio(row.audio, aud_path + row.audio).play().wait().log(),
        newTimer('wait', 3000).start().wait(),

        newFunction('aud4', () => {
            var audio = new Audio(aud_path + 'Press_Spacebar.mp3');
            console.log(audio);
            audio.play();
        }).call(),
        newTimer('wait2', 500).start().wait(),
        newButton('space', 'spacebar').center().print(),
        newTimer('wait3', 1000).start().wait(),

        newKey(' ').wait(),

        clear(),
        newTimer('wait3', 200).start().wait(),

        getMediaRecorder('recorder').stop()
    ).log('trial_type', 'practice')
);

function shuffle(arr) {
    var curr_idx = arr.length, rndm_idx;
  
    while (0 !== curr_idx) {
      rndm_idx = Math.floor(Math.random() * curr_idx);
      curr_idx--;
      [arr[curr_idx], arr[rndm_idx]] = [arr[rndm_idx], arr[curr_idx]];
    }
  
    return arr;
}

// set speakers
options_b = shuffle(['A', 'B', 'C']);
options_w = shuffle(['A', 'B', 'C', 'D']);
names_b = shuffle(['Keisha', 'Raven']);
speaker = dialect == 'AAE' ? {
    'optimal': 'BlackSpeaker_' + options_b.pop() + '.jpg', 
    'intermediate': 'BlackSpeaker_' + options_b.pop() + '.jpg',
    'suboptimal': 'WhiteSpeaker_' + options_w.pop() + '.jpg', 
    'optimal_name': names_b.pop(),
    'intermediate_name': names_b.pop(),
    'suboptimal_name': 'Holly'
} : {
    'optimal': 'WhiteSpeaker_' + options_w.pop() + '.jpg', 
    'intermediate': 'BlackSpeaker_' + options_b.pop() + '.jpg',
    'suboptimal': 'BlackSpeaker_' + options_b.pop() + '.jpg',
    'optimal_name': 'Holly',
    'intermediate_name': names_b.pop(),
    'suboptimal_name': names_b.pop()
}

newTrial('progress1',
    defaultText.center().print(),

    newText('Let’s meet our commanders!'),

    newAudio('CommanderScreen_Intro', aud_path + 'CommanderScreen_Intro.mp3').play().wait().log(),

    newImage('opt_speaker', img_path + speaker['optimal']).center().print(),
    newAudio('Introduction_' + speaker['optimal_name'] + '_AAE.mp3', aud_path + 'Introduction_' + speaker['optimal_name'] + '_AAE.mp3').play().wait().log(),
    getImage('opt_speaker').remove(),

    newImage('int_speaker', img_path + speaker['intermediate']).center().print(),
    newAudio('Introduction_' + speaker['intermediate_name'] + '_GAE_B.mp3', aud_path + 'Introduction_' + speaker['intermediate_name'] + '_GAE_B.mp3').play().wait().log(),
    getImage('int_speaker').remove(),

    newImage('sub_speaker', img_path + speaker['suboptimal']).center().print(),
    newAudio('Introduction_' + speaker['suboptimal_name'] + '_GAE_W.mp3', aud_path + 'Introduction_' + speaker['suboptimal_name'] + '_GAE_W.mp3').play().wait().log(),
    getImage('sub_speaker').remove(),

    newFunction('aud4', () => {
        var audio = new Audio(aud_path + 'Press_Spacebar.mp3');
        console.log(audio);
        audio.play();
    }).call(),
    newTimer('wait5', 800).start().wait(),
    newButton('space', 'spacebar').center().print(),
    newTimer('wait6', 600).start().wait(),
    
    newKey(' ').wait()
);

newTrial('quest1',
    defaultText.center().print(),
    
    newImage('questimg', img_path + 'Reinforcer_QuestMap1.jpg').center().print(),

    newAudio('QuestMap_Mission1', aud_path + 'QuestMap_Mission1.mp3').play().wait().log(),
    
    newFunction('aud4', () => {
        var audio = new Audio(aud_path + 'Press_Spacebar.mp3');
        console.log(audio);
        audio.play();
    }).call(),
    newTimer('wait2', 800).start().wait(),
    
    newButton('space', 'spacebar').center().print(),
    newTimer('wait3', 600).start().wait(),

    newKey(' ').wait()
);

var posns = ['topleft', 'topright', 'bottomleft', 'bottomright'];
var positions = [];
var trials = 56;
for(var i = 0; i < trials; i++) {
    t = shuffle(posns).map((x) => x); // make a copy so there won't be referencing issues
    positions.push(t);
}
var position = 0;
var time = 0;
var images = ['bag1.jpg', 'bag2.jpg', 'bag3.jpg', 'bag4.jpg', 'ball1.jpg', 'ball2.jpg', 'ball3.jpg', 'ball4.jpg', 'bell1.jpg', 'bell2.jpg', 'bell3.jpg', 'bell4.jpg', 'bike1.jpg', 'bike2.jpg', 'bike3.jpg', 'bike4.jpg', 'BlackSpeaker_A.jpg', 'BlackSpeaker_B.jpg', 'BlackSpeaker_C.jpg', 'book1.jpg', 'book2.jpg', 'book3.jpg', 'book4.jpg', 'box1.jpg', 'box2.jpg', 'box3.jpg', 'box4.jpg', 'bread1.jpg', 'bread2.jpg', 'bread3.jpg', 'bread4.jpg', 'brush1.jpg', 'brush2.jpg', 'brush3.jpg', 'brush4.jpg', 'bush1.jpg', 'bush2.jpg', 'bush3.jpg', 'bush4.jpg', 'can1.jpg', 'can2.jpg', 'can3.jpg', 'can4.jpg', 'car1.jpg', 'car2.jpg', 'car3.jpg', 'car4.jpg', 'cart1.jpg', 'cart2.jpg', 'cart3.jpg', 'cart4.jpg', 'cat1.jpg', 'cat2.jpg', 'cat3.jpg', 'cat4.jpg', 'chair1.jpg', 'chair2.jpg', 'chair3.jpg', 'chair4.jpg', 'coat1.jpg', 'coat2.jpg', 'coat3.jpg', 'coat4.jpg', 'cookies1.jpg', 'cookies2.jpg', 'cookies3.jpg', 'cookies4.jpg', 'costume1.jpg', 'costume2.jpg', 'costume3.jpg', 'costume4.jpg', 'couch1.jpg', 'couch2.jpg', 'couch3.jpg', 'couch4.jpg', 'crayon1.jpg', 'crayon2.jpg', 'crayon3.jpg', 'crayon4.jpg', 'dog1.jpg', 'dog2.jpg', 'dog3.jpg', 'dog4.jpg', 'doll1.jpg', 'doll2.jpg', 'doll3.jpg', 'doll4.jpg', 'dress1.jpg', 'dress2.jpg', 'dress3.jpg', 'dress4.jpg', 'football1.jpg', 'football2.jpg', 'football3.jpg', 'football4.jpg', 'footprint1.jpg', 'footprint2.jpg', 'footprint3.jpg', 'footprint4.jpg', 'grapes1.jpg', 'grapes2.jpg', 'grapes3.jpg', 'grapes4.jpg', 'horn1.jpg', 'horn2.jpg', 'horn3.jpg', 'horn4.jpg', 'horse1.jpg', 'horse2.jpg', 'horse3.jpg', 'horse4.jpg', 'IntroExperimentDisplayScreen_a.jpg', 'IntroExperimentDisplayScreen_b.jpg', 'IntroExperimentDisplayScreen_b_pp.jpg', 'jewel1.jpg', 'jewel2.jpg', 'jewel3.jpg', 'jewel4.jpg', 'juice1.jpg', 'juice2.jpg', 'juice3.jpg', 'juice4.jpg', 'kite1.jpg', 'kite2.jpg', 'kite3.jpg', 'kite4.jpg', 'mail1.jpg', 'mail2.jpg', 'mail3.jpg', 'mail4.jpg', 'milk1.jpg', 'milk2.jpg', 'milk3.jpg', 'milk4.jpg', 'mittens1.jpg', 'mittens2.jpg', 'mittens3.jpg', 'mittens4.jpg', 'peanut1.jpg', 'peanut2.jpg', 'peanut3.jpg', 'peanut4.jpg', 'peanut5.jpg', 'peanut6.jpg', 'piano1.jpg', 'piano2.jpg', 'piano3.jpg', 'piano4.jpg', 'pickle1.jpg', 'pickle2.jpg', 'pickle3.jpg', 'pickle4.jpg', 'picture1.jpg', 'picture2.jpg', 'picture3.jpg', 'picture4.jpg', 'planet_blue_screensideselection.jpg', 'planet_orange_screensideselection.jpg', 'plant1.jpg', 'plant2.jpg', 'plant3.jpg', 'plant4.jpg', 'Reinforcer_1a.jpg', 'Reinforcer_1b - Copy.jpg', 'Reinforcer_1b.jpg', 'Reinforcer_1b_pp.jpg', 'Reinforcer_2a.jpg', 'Reinforcer_2b - Copy.jpg', 'Reinforcer_2b.jpg', 'Reinforcer_2b_pp.jpg', 'Reinforcer_3a.jpg', 'Reinforcer_3a_pp.jpg', 'Reinforcer_3b - Copy.jpg', 'Reinforcer_3b.jpg', 'Reinforcer_3b_pp.jpg', 'Reinforcer_4a.jpg', 'Reinforcer_4a_p.jpg', 'Reinforcer_4b.jpg', 'Reinforcer_4b_pp.jpg', 'Reinforcer_5a.jpg', 'Reinforcer_5a_pp.jpg', 'Reinforcer_5b.jpg', 'Reinforcer_5b_pp.jpg', 'Reinforcer_QuestMap1b.jpg', 'Reinforcer_QuestMap1b_pp.jpg', 'Reinforcer_QuestMap1.jpg', 'Reinforcer_QuestMap2b.jpg', 'Reinforcer_QuestMap2b_pp.jpg', 'Reinforcer_QuestMap2.jpg', 'Reinforcer_QuestMap2_pp.jpg', 'Reinforcer_QuestMap3b.jpg', 'Reinforcer_QuestMap3b_pp.jpg', 'Reinforcer_QuestMap3.jpg', 'Reinforcer_QuestMap3_pp.jpg', 'Reinforcer_QuestMap4b.jpg', 'Reinforcer_QuestMap4b_pp.jpg', 'Reinforcer_QuestMap4.jpg', 'Reinforcer_QuestMap4_pp.jpg', 'Reinforcer_QuestMap5b.jpg', 'Reinforcer_QuestMap5b_pp.jpg', 'Reinforcer_QuestMap5.jpg', 'Reinforcer_QuestMap5_pp.jpg', 'ring1.jpg', 'ring1_PhotoShopedited_AS.jpg', 'ring2.jpg', 'ring2_PhotoShopedited_AS.jpg', 'ring3.jpg', 'ring3_PhotoShopedited_AS.jpg', 'ring4.jpg', 'sandwich1.jpg', 'sandwich2.jpg', 'sandwich3.jpg', 'sandwich4.jpg', 'santa1.jpg', 'santa2.jpg', 'santa3.jpg', 'santa4.jpg', 'scissors1.jpg', 'scissors2.jpg', 'scissors3.jpg', 'scissors4.jpg', 'shirt1.jpg', 'shirt2.jpg', 'shirt3.jpg', 'shirt4.jpg', 'shoes1.jpg', 'shoes2.jpg', 'shoes3.jpg', 'shoes4.jpg', 'spacebar.jpg', 'spaceflower.jpg', 'spaceship_blue_screensideselection.jpg', 'spaceship_orange_screensideselection.jpg', 'tractor1.jpg', 'tractor2.jpg', 'tractor3.jpg', 'tractor4.jpg', 'tree1.jpg', 'tree2.jpg', 'tree3.jpg', 'tree4.jpg', 'trophy1.jpg', 'trophy2.jpg', 'trophy3.jpg', 'trophy4.jpg', 'truck1.jpg', 'truck2.jpg', 'truck3.jpg', 'truck4.jpg', 'whistle1.jpg', 'whistle2.jpg', 'whistle3.jpg', 'whistle4.jpg', 'WhiteSpeaker_A.jpg', 'WhiteSpeaker_B.jpg', 'WhiteSpeaker_C.jpg', 'WhiteSpeaker_D.jpg'];
var trial_num = 1;
var counter = 0;

Template(csv, row =>
    PennController('images',
        defaultText.center().print(),

        newVar('trial_num', trial_num),

        getVar('trial_num').value % 11 === 0 ? newImage('reinforcer', img_path + 'Reinforcer_' + (getVar('trial_num').value / 11) + 'a.jpg').center().print() : NaN,
        getVar('trial_num').value % 11 === 0 ? newAudio('Reinforcer_GreatJob', aud_path + 'Reinforcer_GreatJob.mp3').play().wait().log() : NaN,
        getVar('trial_num').value % 11 === 0 ? getImage('reinforcer').remove() : NaN,

        getVar('trial_num').set(parseInt(trial_num++)),

        getVar('trial_num').value % 11 === 0 ? newImage('questimg', img_path + 'Reinforcer_QuestMap' + ((getVar('trial_num').value / 11) + 1) + '_pp.jpg').center().print() : NaN,
        getVar('trial_num').value % 11 === 0 ? newAudio('QuestMap_Mission' + ((getVar('trial_num').value / 11) + 1) + '.mp3', aud_path + 'QuestMap_Mission' + ((getVar('trial_num').value / 11) + 1) + '.mp3').play().wait().log() : NaN,
        
        getVar('trial_num').value % 11 === 0 ? newFunction('space_aud', () => {
            var audio = new Audio(aud_path + 'Press_Spacebar.mp3');
            console.log(audio);
            audio.play();
        }).call() : NaN,
        getVar('trial_num').value % 11 === 0 ? newTimer('wait' + counter++, 800).start().wait() : NaN,
        getVar('trial_num').value % 11 === 0 ? newButton('space', 'spacebar').center().print() : NaN,
        getVar('trial_num').value % 11 === 0 ? newTimer('wait' + counter++, 600).start().wait() : NaN,
        getVar('trial_num').value % 11 === 0 ? newKey(' ').wait() : NaN,
        getVar('trial_num').value % 11 === 0 ? getImage('questimg').remove() : NaN,
        getVar('trial_num').value % 11 === 0 ? getButton('space').remove() : NaN,
        
        newImage('speaker', img_path + speaker[row.Condition]).print(),

        newFunction('aud', () => {
            var audio_file = 'Instructions_';
            if(row.Speaker == 'GAE' && speaker[row.Condition + '_name'] == 'Holly') {
                audio_file += speaker[row.Condition + '_name'] + '_' + row.Speaker + '_W_short.mp3';
            } else if (row.Speaker == 'GAE') {
                audio_file += speaker[row.Condition + '_name'] + '_' + row.Speaker + '_B_short.mp3';
            } else {
                audio_file += speaker[row.Condition + '_name'] + '_' + row.Speaker + '_short.mp3';
            }
            var audio = new Audio(aud_path + audio_file);
            console.log(audio);
            audio.play();
        }).call(),

        newTimer('wait', 1500).start().wait(),
        
        getImage('speaker').remove(),
        
        newMediaRecorder('recorder', 'video').log().record(), // log start time of video
        
        newFunction('aud2', () => {
            var suffix = '';

            if(row.Condition == 'optimal') {
                suffix = '.mp3';
            } else if (row.Condition == 'suboptimal') {
                suffix = '_W.mp3';
            } else {
                suffix = '_B.mp3';
            }
            var audio = new Audio(aud_path + row['Verb-NounAudio'].slice(0, -4) + suffix); 
            console.log(audio);
            audio.play();
        }).call(),

        images.includes(row.TargetImage) ? newImage(positions[position][0], img_path + row.TargetImage).print() : newText('txt1', row.TargetImage + ', pos: ' + positions[position][0]).print(),
        images.includes(row.FoilAImage) ? newImage(positions[position][1], img_path + row.FoilAImage).print() : newText('txt2', row.FoilAImage + ', pos: ' + positions[position][1]).print(),
        images.includes(row.FoilBImage) ? newImage(positions[position][2], img_path + row.FoilBImage).print() : newText('txt3', row.FoilBImage + ', pos: ' + positions[position][2]).print(),
        images.includes(row.FoilCImage) ? newImage(positions[position][3], img_path + row.FoilCImage).print() : newText('txt4', row.FoilCImage + ', pos: ' + positions[position][3]).print(),
        
        newTimer('wait' + counter++, 7000).start().wait(),
        
        newButton('space', 'spacebar').center().print(),
        newKey(' ').wait(),

        newVar('pos', position),
        getVar('pos').set(parseInt(position++)),
        
        getMediaRecorder('recorder').stop()
    ).log('trial_type', 'real').log('trial_num', trial_num).log('condition', row.Condition).log('condition', row.Verb_Type).log('target', row.TargetImage),
);

UploadRecordings('upload');

newTrial('finish',
    defaultText.center().print(),
    newText('<p>Thank You for participating!</p>'),
    SendResults(),
    newText(DownloadRecordingButton(
        "Please click here to download an archive of your recordings: "+
        "we may ask you to send them manually in case there is an issue with the version on our servers."
    )),
    newAudio('ThankYou_Audio', aud_path + 'ThankYou_Audio.mp3').play().wait().log(),
    newButton('waitforever').wait()
);
